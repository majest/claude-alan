--[[
MonsterEffects
A LocalScript. It goes in StarterPlayer > StarterPlayerScripts.

Everything about the monster that happens on your own screen rather than
in the world: the camera shakes when it stomps or roars, the air fills with
dust the nearer it gets, a line at the top of the screen says how far away
it is and which way, and a message appears when it surfaces.

It reads two things the server keeps up to date: the Phase attribute on
NewYorkInfo (calm, surfacing, rampage) and the Stomp counter on the
Monster model, which goes up by one for every footfall and by more for a
roar or the head coming off the statue.
]]

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Lighting = game:GetService("Lighting")

local player = Players.LocalPlayer
local camera = workspace.CurrentCamera
local info = ReplicatedStorage:WaitForChild("NewYorkInfo")
local city = workspace:WaitForChild("NewYork")

local SHAKE_RANGE = 900     -- studs. Closer than this and you feel the footsteps.
local DUST_RANGE = 700      -- closer than this and the air thickens

local function clamp(n, lo, hi)
	if n < lo then return lo end
	if n > hi then return hi end
	return n
end

-- The two lines of text
local gui = Instance.new("ScreenGui")
gui.Name = "MonsterEffects"
gui.ResetOnSpawn = false

local warning = Instance.new("TextLabel")
warning.Size = UDim2.new(0, 460, 0, 28)
warning.Position = UDim2.new(0.5, -230, 0, 12)
warning.BackgroundColor3 = Color3.fromRGB(20, 20, 24)
warning.BackgroundTransparency = 0.3
warning.TextColor3 = Color3.fromRGB(255, 120, 100)
warning.Font = Enum.Font.GothamBold
warning.TextSize = 16
warning.Text = ""
warning.Visible = false
warning.Parent = gui
local corner = Instance.new("UICorner")
corner.CornerRadius = UDim.new(0, 8)
corner.Parent = warning

local message = Instance.new("TextLabel")
message.Size = UDim2.new(1, 0, 0, 60)
message.Position = UDim2.new(0, 0, 0.3, 0)
message.BackgroundTransparency = 1
message.TextColor3 = Color3.fromRGB(255, 230, 230)
message.TextStrokeTransparency = 0.2
message.Font = Enum.Font.GothamBold
message.TextSize = 40
message.Text = ""
message.Visible = false
message.Parent = gui

gui.Parent = player:WaitForChild("PlayerGui")

local messageUntil = 0
local function announce(text, seconds)
	message.Text = text
	message.Visible = true
	messageUntil = os.clock() + seconds
end

local MESSAGES = {
	surfacing = "Something is moving in the harbour.",
	rampage = "IT IS IN THE CITY. RUN.",
}
local lastPhase = info:GetAttribute("Phase")

-- Which way is it? north is -Z and east is -X.
local function compass(d)
	local angle = math.deg(math.atan2(-d.X, -d.Z))   -- 0 north, 90 east
	if angle < 0 then angle = angle + 360 end
	local names = { "north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west" }
	return names[math.floor((angle + 22.5) / 45) % 8 + 1]
end

local atmosphere = Lighting:FindFirstChildOfClass("Atmosphere")
local baseDensity = atmosphere and atmosphere.Density or 0.3
local baseHaze = atmosphere and atmosphere.Haze or 1.5

local lastStomp = 0
local shake = 0

local function findRoot()
	local m = city:FindFirstChild("Monster")
	return m and m:FindFirstChild("Root")
end

RunService:BindToRenderStep("MonsterEffects", Enum.RenderPriority.Camera.Value + 1, function(dt)
	-- the message when the phase changes
	local phase = info:GetAttribute("Phase")
	if phase ~= lastPhase then
		lastPhase = phase
		if MESSAGES[phase] then announce(MESSAGES[phase], 6) end
	end
	if message.Visible and os.clock() > messageUntil then message.Visible = false end

	local root = findRoot()
	local character = player.Character
	local hrp = character and character:FindFirstChild("HumanoidRootPart")
	if not (root and hrp) or phase == "calm" then
		warning.Visible = false
		return
	end

	local d = root.Position - hrp.Position
	local dist = d.Magnitude
	local near = clamp(1 - dist / SHAKE_RANGE, 0, 1)

	-- the distance line
	warning.Visible = true
	warning.Text = string.format("THE MONSTER   %d studs   to the %s", math.floor(dist), compass(d))

	-- every footfall is a jolt, fading over half a second
	local monster = root.Parent
	local stompCount = monster:GetAttribute("Stomp") or 0
	if stompCount ~= lastStomp then
		shake = math.min(shake + (stompCount - lastStomp), 6)
		lastStomp = stompCount
	end
	shake = shake * math.max(0, 1 - dt * 4)
	local amount = shake * near * near * 1.2
	if amount > 0.01 then
		camera.CFrame = camera.CFrame * CFrame.new(
			(math.random() - 0.5) * amount, (math.random() - 0.5) * amount, 0)
	end

	-- dust in the air the nearer it is
	if atmosphere then
		local dust = clamp(1 - dist / DUST_RANGE, 0, 1)
		atmosphere.Density = baseDensity + dust * 0.35
		atmosphere.Haze = baseHaze + dust * 4
	end
end)
