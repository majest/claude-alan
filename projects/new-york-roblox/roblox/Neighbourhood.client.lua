--[[
Neighbourhood
A LocalScript. It goes in StarterPlayer > StarterPlayerScripts.

Shows a box in the bottom-left corner that says where you are:
  Midtown
  5th Ave & W 34th St
It gets all the numbers from the NewYorkInfo folder the server script puts
in ReplicatedStorage, so if the city changes, this changes with it.
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local player = Players.LocalPlayer
local info = ReplicatedStorage:WaitForChild("NewYorkInfo")

local AVE = info:GetAttribute("AvenueSpacing")
local SU = info:GetAttribute("StreetUnit")

-- "s:e:w;s:e:w;..." back into a table
local SHORE = {}
for s, e, w in string.gmatch(info:GetAttribute("Shore"), "([^:;]+):([^:;]+):([^:;]+)") do
	table.insert(SHORE, { s = tonumber(s), e = tonumber(e), w = tonumber(w) })
end

local AVENUES = {}
for name in string.gmatch(info:GetAttribute("Avenues"), "[^;]+") do
	table.insert(AVENUES, name)
end

local BORDER = {}
for n in string.gmatch(info:GetAttribute("Border"), "[^,]+") do
	table.insert(BORDER, tonumber(n))
end

local ZONES = {}
for _, f in ipairs(info:GetChildren()) do
	table.insert(ZONES, {
		name = f.Name, kind = f:GetAttribute("Kind"), order = f:GetAttribute("Order"), park = f:GetAttribute("Park"),
		s1 = f:GetAttribute("S1"), s2 = f:GetAttribute("S2"),
		a1 = f:GetAttribute("A1"), a2 = f:GetAttribute("A2"),
	})
end
table.sort(ZONES, function(p, q) return p.order < q.order end)

local function shoreAt(s)
	if s <= SHORE[1].s then return SHORE[1].e, SHORE[1].w end
	for i = 2, #SHORE do
		local p, q = SHORE[i - 1], SHORE[i]
		if s <= q.s then
			local t = (s - p.s) / (q.s - p.s)
			return p.e + (q.e - p.e) * t, p.w + (q.w - p.w) * t
		end
	end
	return SHORE[#SHORE].e, SHORE[#SHORE].w
end

local function round(n) return math.floor(n + 0.5) end

local function ordinal(n)
	local last, lastTwo = n % 10, n % 100
	if lastTwo >= 11 and lastTwo <= 13 then return n .. "th" end
	if last == 1 then return n .. "st" end
	if last == 2 then return n .. "nd" end
	if last == 3 then return n .. "rd" end
	return n .. "th"
end

-- The nearest corner, like "5th Ave & W 34th St"
local function corner(a, s, park)
	local avenue = AVENUES[round(a)]
	local street = round(s)
	if street < 1 then return "Lower Manhattan" end
	local side = ""                           -- 5th Avenue is where east turns into west
	if round(a) > 7 then side = "W " elseif round(a) < 7 then side = "E " end
	if park or not avenue then return "near " .. side .. ordinal(street) .. " St" end
	return avenue .. " & " .. side .. ordinal(street) .. " St"
end

local function whereAmI(x, z)
	local a, s = x / AVE, -z / SU
	local e, w = shoreAt(s)
	local onIsland = s >= SHORE[1].s and s <= SHORE[#SHORE].s and a >= e and a <= w
	for _, zone in ipairs(ZONES) do
		local inside = s >= zone.s1 and s < zone.s2 and a >= zone.a1 and a < zone.a2
		if inside and ((zone.kind == "island") == onIsland) then
			if onIsland then return zone.name, corner(a, s, zone.park) end
			return zone.name, ""
		end
	end
	if x < BORDER[1] or x > BORDER[2] or z < BORDER[3] or z > BORDER[4] then
		return "Beyond the border", ""
	end
	if s < -26 then return "New York Harbor", "" end
	if a < e then return (s > 120) and "Harlem River" or "East River", "" end
	if a > w then return "Hudson River", "" end
	return "Somewhere wet", ""
end

-- The box on screen
local gui = Instance.new("ScreenGui")
gui.Name = "Neighbourhood"
gui.ResetOnSpawn = false

local frame = Instance.new("Frame")
frame.Size = UDim2.new(0, 260, 0, 64)
frame.Position = UDim2.new(0, 16, 1, -80)
frame.BackgroundColor3 = Color3.fromRGB(20, 20, 24)
frame.BackgroundTransparency = 0.25
frame.BorderSizePixel = 0
frame.Parent = gui

local rounded = Instance.new("UICorner")
rounded.CornerRadius = UDim.new(0, 10)
rounded.Parent = frame

local big = Instance.new("TextLabel")
big.Size = UDim2.new(1, -20, 0, 30)
big.Position = UDim2.new(0, 10, 0, 6)
big.BackgroundTransparency = 1
big.Font = Enum.Font.GothamBold
big.TextSize = 22
big.TextColor3 = Color3.fromRGB(255, 255, 255)
big.TextXAlignment = Enum.TextXAlignment.Left
big.TextScaled = false
big.Text = ""
big.Parent = frame

local small = Instance.new("TextLabel")
small.Size = UDim2.new(1, -20, 0, 20)
small.Position = UDim2.new(0, 10, 0, 36)
small.BackgroundTransparency = 1
small.Font = Enum.Font.Gotham
small.TextSize = 15
small.TextColor3 = Color3.fromRGB(200, 210, 220)
small.TextXAlignment = Enum.TextXAlignment.Left
small.Text = ""
small.Parent = frame

gui.Parent = player:WaitForChild("PlayerGui")

while true do
	local character = player.Character
	local rootPart = character and character:FindFirstChild("HumanoidRootPart")
	if rootPart then
		local p = rootPart.Position
		local name, detail = whereAmI(p.X, p.Z)
		big.Text = name
		small.Text = detail
	end
	task.wait(0.3)
end
