--[[
TaxiDriver
A LocalScript. It goes in StarterPlayer > StarterPlayerScripts.

Drives the taxis. When you sit in a taxi's seat, this starts running every
frame: it reads the seat's Throttle and Steer (which Roblox fills in from
W A S D, the arrow keys, or the thumbstick on a phone) and sets the two
constraints on the car that push it along and turn it.

It runs on the driver's own computer rather than the server on purpose.
The server hands the car's physics to the driver the moment they sit down,
so what this script does takes effect at once, with no round trip to the
server and back. That is what makes steering feel instant.

Space gets you out, which is how every seat in Roblox works.
]]

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local player = Players.LocalPlayer

local MAX_SPEED = 90      -- studs per second. A character runs at 16.
local REVERSE_SPEED = 30
local ACCEL = 45          -- studs per second, per second
local BRAKE = 90
local COAST = 25          -- how fast it slows with no key held
local TURN = 1.7          -- radians per second at full speed

local driving = nil       -- the car being driven right now, or nil

local function clamp(n, lo, hi)
	if n < lo then return lo end
	if n > hi then return hi end
	return n
end

-- The hint that shows while you drive
local gui = Instance.new("ScreenGui")
gui.Name = "TaxiHint"
gui.ResetOnSpawn = false
local hint = Instance.new("TextLabel")
hint.Size = UDim2.new(0, 420, 0, 34)
hint.Position = UDim2.new(0.5, -210, 1, -50)
hint.BackgroundColor3 = Color3.fromRGB(255, 200, 30)
hint.BackgroundTransparency = 0.1
hint.TextColor3 = Color3.fromRGB(30, 25, 0)
hint.Font = Enum.Font.GothamBold
hint.TextSize = 16
hint.Text = "W / S  drive      A / D  steer      Space  get out"
hint.Visible = false
hint.Parent = gui
local rounded = Instance.new("UICorner")
rounded.CornerRadius = UDim.new(0, 8)
rounded.Parent = hint
gui.Parent = player:WaitForChild("PlayerGui")

local function stopDriving()
	if driving then
		driving.push.PlaneVelocity = Vector2.new(0, 0)
		driving.turn.AngularVelocity = Vector3.new(0, 0, 0)
	end
	driving = nil
	hint.Visible = false
end

local function startDriving(seat)
	local car = seat.Parent
	local chassis = car and car:FindFirstChild("Chassis")
	local push = chassis and chassis:FindFirstChild("Push")
	local turn = chassis and chassis:FindFirstChild("Turn")
	if not (push and turn) then return end
	driving = { seat = seat, push = push, turn = turn, speed = 0 }
	hint.Visible = true
end

-- Every frame while driving
RunService.RenderStepped:Connect(function(dt)
	local d = driving
	if not d then return end
	local throttle, steer = d.seat.ThrottleFloat, d.seat.SteerFloat

	if throttle > 0 then
		d.speed = math.min(d.speed + ACCEL * throttle * dt, MAX_SPEED)
	elseif throttle < 0 then
		if d.speed > 0 then
			d.speed = math.max(d.speed - BRAKE * dt, 0)              -- brake first...
		else
			d.speed = math.max(d.speed - ACCEL * 0.6 * dt, -REVERSE_SPEED)   -- ...then reverse
		end
	else
		if d.speed > 0 then
			d.speed = math.max(d.speed - COAST * dt, 0)
		else
			d.speed = math.min(d.speed + COAST * dt, 0)
		end
	end

	-- You cannot turn a car that is standing still, and in reverse the
	-- steering goes the other way. Scaling by speed does both.
	local grip = clamp(d.speed / (MAX_SPEED * 0.4), -1, 1)
	local yaw = -steer * TURN * grip

	d.push.PlaneVelocity = Vector2.new(d.speed, 0)
	d.turn.AngularVelocity = Vector3.new(0, yaw, 0)
end)

-- Notice when this player sits down in, or gets out of, a taxi
local function watch(character)
	local humanoid = character:WaitForChild("Humanoid")
	humanoid.Seated:Connect(function(active, seat)
		local car = seat and seat.Parent
		if active and seat:IsA("VehicleSeat") and car and car:GetAttribute("Taxi") then
			startDriving(seat)
		else
			stopDriving()
		end
	end)
end

if player.Character then watch(player.Character) end
player.CharacterAdded:Connect(watch)
