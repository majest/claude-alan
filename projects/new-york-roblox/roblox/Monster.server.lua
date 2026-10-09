--[[
Monster
A Script. It goes in ServerScriptService, next to BuildNewYork.

The reason the game exists. A minute after the server starts, something
comes up out of the harbour, tears the head off the Statue of Liberty and
throws it into the Financial District, then walks up Manhattan. Anything it
walks through is knocked loose and topples. Anything under a hand or a foot
dies. It comes for any player it can see, and the parasites that drop off it
come for everyone else.

There is no recorded animation. The body is moved along by the brain at the
bottom of this file, and the limbs are worked out every frame: a hand or a
foot stays planted on the ground until the body has moved too far from it,
then it lifts and steps forward. The elbows and knees are worked out from
where the hands and feet are. That is why it lurches, which is right.

It waits for BuildNewYork to finish, so it can find the city, the folders
of buildings it is allowed to knock over, and the statue's head.
]]

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Debris = game:GetService("Debris")

local CONFIG = {
	DELAY = 60,            -- seconds after the server starts before it surfaces
	HEIGHT = 120,          -- to the top of its back, in studs. Everything scales with this.
	WALK_SPEED = 22,       -- studs per second. A player runs at 16, a taxi does 90.
	CHASE_SPEED = 30,
	CHASE_RANGE = 450,     -- it comes for a player within this
	TURN_RATE = 0.7,       -- radians per second. Big things turn slowly.
	STEP_HEIGHT = 28,
	SMASH_LIMIT = 14,      -- buildings knocked over by one stomp, at most
	PARASITES_MAX = 8,
	PARASITE_EVERY = 25,   -- seconds between drops
	PARASITE_SPEED = 15,   -- a touch slower than a running player
	PARASITE_LIFE = 120,
	PARASITE_BITE = 12,
}

-- ---------------------------------------------------------------------------
-- Wait for the city, then find the bits of it this script needs.
-- ---------------------------------------------------------------------------

local info = ReplicatedStorage:WaitForChild("NewYorkInfo")
local city = workspace:WaitForChild("NewYork")
local AVE = info:GetAttribute("AvenueSpacing")
local SU = info:GetAttribute("StreetUnit")
local function xOf(a) return a * AVE end
local function zOf(s) return -s * SU end

local smashable = {}
for _, name in ipairs({ "Buildings", "Boroughs", "Bridges", "Landmarks", "Parks" }) do
	local f = city:FindFirstChild(name)
	if f then table.insert(smashable, f) end
end
local landmarks = city:FindFirstChild("Landmarks")
local libertyHead = landmarks and landmarks:FindFirstChild("LibertyHead")

local rng = Random.new(7)
local u = CONFIG.HEIGHT / 120   -- the body below is drawn for a 120-stud monster, then scaled

-- ---------------------------------------------------------------------------
-- The body. Offsets are in the monster's own space: it stands at the origin,
-- facing -Z, feet on the ground, before being scaled by u.
-- ---------------------------------------------------------------------------

local SKIN = Color3.fromRGB(140, 132, 118)
local DARK = Color3.fromRGB(95, 88, 78)
local PINK = Color3.fromRGB(120, 70, 70)

local monster = Instance.new("Model")
monster.Name = "Monster"
monster:SetAttribute("Stomp", 0)

local function mk(class, name, size, colour, material, collide)
	local p = Instance.new(class)
	p.Name = name
	p.Size = size * u
	p.Color = colour
	p.Material = material
	p.Anchored = true
	p.CanCollide = collide == true
	p.CastShadow = true
	p.TopSurface = Enum.SurfaceType.Smooth
	p.BottomSurface = Enum.SurfaceType.Smooth
	p.CFrame = CFrame.new(0, -1000, 0)
	p.Parent = monster
	return p
end

local root = mk("Part", "Root", Vector3.new(4, 4, 4), SKIN, Enum.Material.SmoothPlastic)
root.Transparency = 1
monster.PrimaryPart = root

local torso = mk("Part", "Torso", Vector3.new(34, 40, 70), SKIN, Enum.Material.Sand)
local hips = mk("Part", "Hips", Vector3.new(26, 24, 30), SKIN, Enum.Material.Sand)
local neck = mk("Part", "Neck", Vector3.new(12, 12, 30), SKIN, Enum.Material.Sand)
local head = mk("Part", "Head", Vector3.new(18, 16, 26), SKIN, Enum.Material.Sand)
local jaw = mk("Part", "Jaw", Vector3.new(14, 5, 20), PINK, Enum.Material.Sand)
local eyeL = mk("Part", "EyeL", Vector3.new(3, 3, 3), Color3.fromRGB(20, 20, 20), Enum.Material.Glass)
local eyeR = mk("Part", "EyeR", Vector3.new(3, 3, 3), Color3.fromRGB(20, 20, 20), Enum.Material.Glass)
eyeL.Shape = Enum.PartType.Ball
eyeR.Shape = Enum.PartType.Ball
local finA = mk("WedgePart", "FinA", Vector3.new(6, 22, 26), DARK, Enum.Material.Sand)
local finB = mk("WedgePart", "FinB", Vector3.new(6, 16, 20), DARK, Enum.Material.Sand)

-- Four limbs. socket: where it joins the body. rest: where the hand or foot
-- wants to be, on the ground. len: the length of each of the two bones.
-- bend: which way the elbow or knee goes. Limbs step in diagonal pairs,
-- front-left with back-right, like a trotting dog.
local LIMBS = {
	{ name = "LH", socket = Vector3.new(-20, 92, -22), rest = Vector3.new(-30, 0, -58), len = 62, bend = Vector3.new(-0.8, 0.6, -0.3), pair = "A", thick = 9, tip = Vector3.new(14, 6, 18) },
	{ name = "RH", socket = Vector3.new(20, 92, -22),  rest = Vector3.new(30, 0, -58),  len = 62, bend = Vector3.new(0.8, 0.6, -0.3),  pair = "B", thick = 9, tip = Vector3.new(14, 6, 18) },
	{ name = "LF", socket = Vector3.new(-13, 56, 30),  rest = Vector3.new(-18, 0, 38),  len = 32, bend = Vector3.new(-0.5, 0.3, 0.8),  pair = "B", thick = 8, tip = Vector3.new(12, 6, 18) },
	{ name = "RF", socket = Vector3.new(13, 56, 30),   rest = Vector3.new(18, 0, 38),   len = 32, bend = Vector3.new(0.5, 0.3, 0.8),   pair = "A", thick = 8, tip = Vector3.new(12, 6, 18) },
}
for _, limb in ipairs(LIMBS) do
	limb.upper = mk("Part", limb.name .. "Upper", Vector3.new(limb.thick, limb.thick, limb.len), SKIN, Enum.Material.Sand)
	limb.lower = mk("Part", limb.name .. "Lower", Vector3.new(limb.thick * 0.8, limb.thick * 0.8, limb.len), SKIN, Enum.Material.Sand)
	limb.foot = mk("Part", limb.name .. "Foot", limb.tip, DARK, Enum.Material.Slate, true)
	limb.planted = nil      -- world position of the foot while it is on the ground
	limb.step = nil         -- { from, to, t } while it is in the air
end

local TAIL_SEGMENTS = 6
local tail = {}
for i = 1, TAIL_SEGMENTS do
	local t = 12 - i * 1.6
	tail[i] = mk("Part", "Tail" .. i, Vector3.new(t, t, 20), SKIN, Enum.Material.Sand)
end

monster.Parent = city

-- ---------------------------------------------------------------------------
-- Maths helpers.
-- ---------------------------------------------------------------------------

local function clamp(n, lo, hi)
	if n < lo then return lo end
	if n > hi then return hi end
	return n
end

local function flat(v) return Vector3.new(v.X, 0, v.Z) end

-- A bar between two world points, like the bridge cables in BuildNewYork.
local function placeBeam(part, a, b)
	if (b - a).Magnitude < 0.5 then b = a + Vector3.new(0, 0.5, 0) end
	part.CFrame = CFrame.lookAt((a + b) / 2, b)
end

-- Two bones of length L from S, with the tip at T. Finds the elbow.
local function solve(S, T, L, bend)
	local d = T - S
	local dist = d.Magnitude
	local reach = 2 * L * 0.98
	if dist > reach then
		T = S + d.Unit * reach
		d = T - S
		dist = reach
	end
	if dist < 1 then
		d = Vector3.new(0, -1, 0)
		dist = 1
	end
	local axis = d / dist
	local perp = bend - axis * bend:Dot(axis)
	if perp.Magnitude < 0.01 then perp = Vector3.new(1, 0, 0) end
	perp = perp.Unit
	local h = math.sqrt(math.max(L * L - (dist / 2) * (dist / 2), 0))
	return S + axis * (dist / 2) + perp * h, T
end

-- ---------------------------------------------------------------------------
-- What it does to the city and the people in it.
-- ---------------------------------------------------------------------------

local smashParams = OverlapParams.new()
smashParams.FilterType = Enum.RaycastFilterType.Include
smashParams.FilterDescendantsInstances = smashable
smashParams.MaxParts = CONFIG.SMASH_LIMIT

local killParams = OverlapParams.new()
killParams.FilterType = Enum.RaycastFilterType.Include

-- Knock loose whatever this part is inside. Anchored buildings become
-- physics objects and topple; they are tidied away half a minute later.
local function smash(part, from)
	for _, hit in ipairs(workspace:GetPartsInPart(part, smashParams)) do
		if hit.Anchored then
			hit.Anchored = false
			local away = flat(hit.Position - from)
			if away.Magnitude < 1 then away = Vector3.new(1, 0, 0) end
			hit.AssemblyLinearVelocity = away.Unit * 35 + Vector3.new(0, 25, 0)
			Debris:AddItem(hit, 30)
		end
	end
end

local function characters()
	local list = {}
	for _, player in ipairs(Players:GetPlayers()) do
		if player.Character then table.insert(list, player.Character) end
	end
	return list
end

-- Anyone inside this part is dead.
local function crush(part)
	local chars = characters()
	if #chars == 0 then return end
	killParams.FilterDescendantsInstances = chars
	for _, hit in ipairs(workspace:GetPartsInPart(part, killParams)) do
		local humanoid = hit.Parent and hit.Parent:FindFirstChildOfClass("Humanoid")
		if humanoid then humanoid.Health = 0 end
	end
end

local function stomp(foot)
	monster:SetAttribute("Stomp", monster:GetAttribute("Stomp") + 1)
	smash(foot, foot.Position)
	crush(foot)
end

local function throwHead()
	if not libertyHead or not libertyHead.Anchored then return end
	local target = Vector3.new(xOf(7), 0, zOf(-15))         -- Wall Street
	local away = flat(target - libertyHead.Position)
	local dist = math.max(away.Magnitude, 1)
	local v = math.sqrt(dist * workspace.Gravity)            -- thrown at 45 degrees, it lands at `dist`
	libertyHead.Anchored = false
	libertyHead.CanCollide = true
	libertyHead.AssemblyLinearVelocity = away.Unit * (v / math.sqrt(2)) + Vector3.new(0, v / math.sqrt(2), 0)
	monster:SetAttribute("Stomp", monster:GetAttribute("Stomp") + 6)   -- a big shake for the clients
end

-- ---------------------------------------------------------------------------
-- Parasites.
-- ---------------------------------------------------------------------------

local parasites = {}

local function spawnParasite(at)
	local m = Instance.new("Model")
	m.Name = "Parasite"
	local function piece(name, size, colour)
		local p = Instance.new("Part")
		p.Name = name
		p.Size = size
		p.Color = colour
		p.Material = Enum.Material.Slate
		p.Anchored = true
		p.CanCollide = false
		p.TopSurface = Enum.SurfaceType.Smooth
		p.BottomSurface = Enum.SurfaceType.Smooth
		p.CFrame = CFrame.new(at)
		p.Parent = m
		return p
	end
	local body = piece("Body", Vector3.new(5, 3, 8), Color3.fromRGB(70, 60, 60))
	local pHead = piece("Head", Vector3.new(4, 3, 4), PINK)
	local legs = {}
	for i = 1, 4 do legs[i] = piece("Leg" .. i, Vector3.new(1, 1, 7), Color3.fromRGB(50, 45, 45)) end
	m.PrimaryPart = body
	m.Parent = city
	table.insert(parasites, { model = m, body = body, head = pHead, legs = legs, pos = at, yaw = 0, born = 0, bit = 0, age = 0 })
end

local function nearestCharacter(from, range)
	local best, bestDist = nil, range
	for _, char in ipairs(characters()) do
		local hrp = char:FindFirstChild("HumanoidRootPart")
		local humanoid = char:FindFirstChildOfClass("Humanoid")
		if hrp and humanoid and humanoid.Health > 0 then
			local d = (hrp.Position - from).Magnitude
			if d < bestDist then best, bestDist = char, d end
		end
	end
	return best, bestDist
end

local function stepParasites(dt, now)
	for i = #parasites, 1, -1 do
		local p = parasites[i]
		p.age = p.age + dt
		if p.age > CONFIG.PARASITE_LIFE then
			p.model:Destroy()
			table.remove(parasites, i)
		else
			local target, dist = nearestCharacter(p.pos, 300)
			local groundY = 1
			if target then
				local hrp = target:FindFirstChild("HumanoidRootPart")
				local to = flat(hrp.Position - p.pos)
				groundY = hrp.Position.Y - 2
				if to.Magnitude > 4 then
					p.yaw = math.atan2(-to.X, -to.Z)
					p.pos = p.pos + to.Unit * CONFIG.PARASITE_SPEED * dt
				elseif now - p.bit > 0.6 then
					p.bit = now
					local humanoid = target:FindFirstChildOfClass("Humanoid")
					if humanoid then humanoid:TakeDamage(CONFIG.PARASITE_BITE) end
				end
			end
			p.pos = Vector3.new(p.pos.X, groundY + 1.5 + math.abs(math.sin(now * 14)) * 0.6, p.pos.Z)
			local cf = CFrame.new(p.pos) * CFrame.Angles(0, p.yaw, 0)
			p.body.CFrame = cf
			p.head.CFrame = cf * CFrame.new(0, 1, -5)
			for k, leg in ipairs(p.legs) do
				local side = (k % 2 == 0) and 1 or -1
				local fore = (k <= 2) and -2 or 2
				local swing = math.sin(now * 14 + k * 1.6) * 2
				local a = (cf * CFrame.new(side * 2, 0, fore)).Position
				local b = (cf * CFrame.new(side * 4, -2, fore + swing)).Position
				placeBeam(leg, a, b)
			end
		end
	end
end

-- ---------------------------------------------------------------------------
-- The brain.
-- ---------------------------------------------------------------------------

-- Places it wanders between, in avenue units and street numbers.
local WAYPOINTS = {
	{ 7.5, -24 }, { 7, -15 }, { 5, -16 }, { 12, -12 }, { 2, 10 }, { 7, 5 }, { 7.5, 23 }, { 7.5, 35 },
	{ 9, 43 }, { 5.5, 43 }, { 7.5, 50 }, { 11, 30 }, { 8.5, 62 }, { 4, 70 }, { 12, 90 }, { 9, 115 },
}

local statueAt = Vector3.new(xOf(16.5), 0, zOf(-62))
local state = "waiting"       -- waiting -> surfacing -> statue -> rampage
local pos = statueAt + Vector3.new(0, -110 * u, 23 * SU)   -- out at sea, under the water, south of the statue
local yaw = math.pi            -- facing south, away from the city, to begin with
local target = statueAt
local waypoint = 1
local now = 0
local sinceParasite = 0
local roarUntil = -1
local nextRoar = 8
local smashTimer = 0
info:SetAttribute("Phase", "calm")

local function forward() return Vector3.new(-math.sin(yaw), 0, -math.cos(yaw)) end

-- Turn towards `to`, no faster than TURN_RATE, and walk at `speed`.
local function moveTowards(to, speed, dt)
	local d = flat(to - pos)
	if d.Magnitude < 1 then return end
	local wantYaw = math.atan2(-d.X, -d.Z)
	local diff = wantYaw - yaw
	while diff > math.pi do diff = diff - 2 * math.pi end
	while diff < -math.pi do diff = diff + 2 * math.pi end
	yaw = yaw + clamp(diff, -CONFIG.TURN_RATE * dt, CONFIG.TURN_RATE * dt)
	pos = pos + forward() * math.min(speed * dt, d.Magnitude)
end

local function think(dt)
	if state == "waiting" then
		if now >= CONFIG.DELAY then
			state = "surfacing"
			info:SetAttribute("Phase", "surfacing")
		end
	elseif state == "surfacing" then
		-- rise out of the sea over about ten seconds while turning for the statue
		pos = Vector3.new(pos.X, math.min(pos.Y + 11 * u * dt, 0), pos.Z)
		moveTowards(statueAt, CONFIG.WALK_SPEED * 0.5, dt)
		if pos.Y >= 0 then state = "statue" end
	elseif state == "statue" then
		moveTowards(statueAt, CONFIG.WALK_SPEED, dt)
		if flat(statueAt - pos).Magnitude < 70 * u then
			throwHead()
			state = "rampage"
			info:SetAttribute("Phase", "rampage")
			target = Vector3.new(xOf(WAYPOINTS[1][1]), 0, zOf(WAYPOINTS[1][2]))
		end
	elseif state == "rampage" then
		local victim, dist = nearestCharacter(pos, CONFIG.CHASE_RANGE)
		if victim then
			local hrp = victim:FindFirstChild("HumanoidRootPart")
			moveTowards(hrp.Position, CONFIG.CHASE_SPEED, dt)
		else
			if flat(target - pos).Magnitude < 40 then
				local pick = waypoint
				while pick == waypoint do pick = rng:NextInteger(1, #WAYPOINTS) end
				waypoint = pick
				target = Vector3.new(xOf(WAYPOINTS[pick][1]), 0, zOf(WAYPOINTS[pick][2]))
			end
			moveTowards(target, CONFIG.WALK_SPEED, dt)
		end
		-- the body sweeps through anything tall every half second
		smashTimer = smashTimer + dt
		if smashTimer > 0.5 then
			smashTimer = 0
			smash(torso, pos)
			smash(hips, pos)
		end
		-- parasites drop off it when someone is near enough to care
		sinceParasite = sinceParasite + dt
		if sinceParasite > CONFIG.PARASITE_EVERY and #parasites < CONFIG.PARASITES_MAX and nearestCharacter(pos, 500) then
			sinceParasite = 0
			spawnParasite(pos + Vector3.new(rng:NextNumber(-20, 20), 2, rng:NextNumber(-20, 20)) * u)
		end
		-- a roar now and then: the jaw drops and the clients shake
		if now > nextRoar then
			nextRoar = now + rng:NextNumber(7, 14)
			roarUntil = now + 1.6
			monster:SetAttribute("Stomp", monster:GetAttribute("Stomp") + 3)
		end
	end
end

-- ---------------------------------------------------------------------------
-- Putting the body where the brain says, every frame.
-- ---------------------------------------------------------------------------

local function pose(dt)
	local walking = state ~= "waiting"
	local bob = walking and math.sin(now * 2.5) * 2 * u or 0
	local body = CFrame.new(pos + Vector3.new(0, bob, 0)) * CFrame.Angles(0, yaw, 0)
	local fwd = forward()

	-- the trunk
	torso.CFrame = body * CFrame.new(Vector3.new(0, 85, -5) * u) * CFrame.Angles(math.rad(-10), 0, 0)
	hips.CFrame = body * CFrame.new(Vector3.new(0, 60, 30) * u)
	finA.CFrame = body * CFrame.new(Vector3.new(0, 112, 5) * u) * CFrame.Angles(0, math.rad(180), 0)
	finB.CFrame = body * CFrame.new(Vector3.new(0, 80, 40) * u) * CFrame.Angles(0, math.rad(180), 0)

	-- the head looks about, and the jaw hangs open when it roars
	local look = math.sin(now * 0.9) * 0.3
	local roaring = now < roarUntil
	local headCF = body * CFrame.new(Vector3.new(0, 78, -70) * u) * CFrame.Angles(roaring and math.rad(-15) or 0, look, 0)
	head.CFrame = headCF
	neck.CFrame = body * CFrame.new(Vector3.new(0, 88, -48) * u) * CFrame.Angles(math.rad(25), 0, 0)
	jaw.CFrame = headCF * CFrame.new(Vector3.new(0, roaring and -12 or -8, -4) * u) * CFrame.Angles(roaring and math.rad(20) or 0, 0, 0)
	eyeL.CFrame = headCF * CFrame.new(Vector3.new(-8, 3, -6) * u)
	eyeR.CFrame = headCF * CFrame.new(Vector3.new(8, 3, -6) * u)

	-- the limbs: planted until the body has moved too far, then a step
	local stepping = { A = false, B = false }
	for _, limb in ipairs(LIMBS) do
		if limb.step then stepping[limb.pair] = true end
	end
	for _, limb in ipairs(LIMBS) do
		local socket = (body * CFrame.new(limb.socket * u)).Position
		local ideal = (body * CFrame.new(limb.rest * u)).Position
		ideal = Vector3.new(ideal.X, 0, ideal.Z)
		if not limb.planted then limb.planted = ideal end
		local other = limb.pair == "A" and "B" or "A"
		if limb.step then
			local s = limb.step
			s.t = math.min(s.t + dt / 0.45, 1)
			local lift = math.sin(s.t * math.pi) * CONFIG.STEP_HEIGHT * u
			limb.planted = s.from + (s.to - s.from) * s.t + Vector3.new(0, lift, 0)
			if s.t >= 1 then
				limb.planted = s.to
				limb.step = nil
				if walking then stomp(limb.foot) end
			end
		elseif walking and not stepping[other] and flat(ideal - limb.planted).Magnitude > 26 * u then
			limb.step = { from = limb.planted, to = ideal + fwd * 22 * u, t = 0 }
			stepping[limb.pair] = true
		end
		-- underwater or rising, the feet simply hang below the body
		local tip = limb.planted
		if state == "waiting" or state == "surfacing" then
			tip = ideal + Vector3.new(0, pos.Y, 0)
		end
		local elbow, hand = solve(socket, tip, limb.len * u, limb.bend)
		placeBeam(limb.upper, socket, elbow)
		placeBeam(limb.lower, elbow, hand)
		limb.foot.CFrame = CFrame.new(hand + Vector3.new(0, 3 * u, 0)) * CFrame.Angles(0, yaw, 0)
	end

	-- the tail: each segment hangs off the last and waves a little later
	local joint = Vector3.new(0, 62, 44) * u
	local dir = Vector3.new(0, -0.25, 1)
	for i, seg in ipairs(tail) do
		local wave = math.sin(now * 2 - i * 0.7) * 0.35 * (walking and 1 or 0.3)
		local d = Vector3.new(dir.X + wave, dir.Y - 0.05 * i, dir.Z).Unit
		local nextJoint = joint + d * 20 * u
		placeBeam(seg, (body * CFrame.new(joint)).Position, (body * CFrame.new(nextJoint)).Position)
		joint = nextJoint
	end

	root.CFrame = body
end

RunService.Heartbeat:Connect(function(dt)
	dt = math.min(dt, 0.1)
	now = now + dt
	think(dt)
	pose(dt)
	stepParasites(dt, now)
end)

print("Monster: waiting. It surfaces in " .. CONFIG.DELAY .. " seconds.")
