#!/usr/bin/env python3
"""Run the Roblox scripts in a pretend Roblox, without Roblox.

    python3 tools/check.py

Roblox Studio is the only thing that can really run these scripts. This
builds a fake copy of the bits of Roblox the scripts use (Instance.new,
Vector3, CFrame, Enum, Terrain, ...) and runs the real scripts on it. It
catches the mistakes that actually happen: a property name spelt wrong, a
material that does not exist, a part bigger than 2048 studs, a number that
came out as nan, a table that was nil.

It cannot tell you whether the city looks good. Only Studio can do that.

Needs the `lupa` module:  pip install lupa
"""

import pathlib
import sys

try:
    from lupa import LuaRuntime
except ImportError:
    sys.exit("needs lupa:  pip install lupa")

HERE = pathlib.Path(__file__).resolve().parent.parent
SERVER = HERE / "roblox" / "BuildNewYork.server.lua"
CLIENT = HERE / "roblox" / "Neighbourhood.client.lua"

MOCK = r"""
-- =========================================================================
-- A pretend Roblox. Just enough of it for these two scripts.
-- =========================================================================
local checks = { parts = 0, errors = {}, byFolder = {}, terrainVolume = 0, fills = 0 }
local function fail(msg) table.insert(checks.errors, msg) end

local function finite(n) return type(n) == "number" and n == n and n ~= math.huge and n ~= -math.huge end

-- Vector3 ---------------------------------------------------------------
local Vector3 = {}
local V3 = {}
V3.__index = function(v, k)
    if k == "Magnitude" then return math.sqrt(v.X * v.X + v.Y * v.Y + v.Z * v.Z) end
    if k == "Unit" then local m = v.Magnitude; return Vector3.new(v.X / m, v.Y / m, v.Z / m) end
    return V3[k]
end
V3.__add = function(a, b) return Vector3.new(a.X + b.X, a.Y + b.Y, a.Z + b.Z) end
V3.__sub = function(a, b) return Vector3.new(a.X - b.X, a.Y - b.Y, a.Z - b.Z) end
V3.__unm = function(a) return Vector3.new(-a.X, -a.Y, -a.Z) end
V3.__mul = function(a, b)
    if type(a) == "number" then return Vector3.new(a * b.X, a * b.Y, a * b.Z) end
    if type(b) == "number" then return Vector3.new(a.X * b, a.Y * b, a.Z * b) end
    return Vector3.new(a.X * b.X, a.Y * b.Y, a.Z * b.Z)
end
V3.__div = function(a, b)
    if type(b) == "number" then return Vector3.new(a.X / b, a.Y / b, a.Z / b) end
    return Vector3.new(a.X / b.X, a.Y / b.Y, a.Z / b.Z)
end
V3.__tostring = function(v) return string.format("(%g, %g, %g)", v.X, v.Y, v.Z) end
function Vector3.new(x, y, z)
    x, y, z = x or 0, y or 0, z or 0
    if not (finite(x) and finite(y) and finite(z)) then fail("Vector3 with a bad number: " .. tostring(x) .. "," .. tostring(y) .. "," .. tostring(z)) end
    return setmetatable({ X = x, Y = y, Z = z, __isVector3 = true }, V3)
end

-- CFrame (position only; rotation is accepted and ignored) -----------------
local CFrame = {}
local CF = {}
CF.__index = CF
CF.__mul = function(a, b)
    if b.__isCFrame then return CFrame.new(a.Position + b.Position) end
    return a.Position + b
end
function CFrame.new(x, y, z)
    if x == nil then return setmetatable({ Position = Vector3.new(0, 0, 0), __isCFrame = true }, CF) end
    if type(x) == "table" and x.__isVector3 then return setmetatable({ Position = x, __isCFrame = true }, CF) end
    return setmetatable({ Position = Vector3.new(x, y, z), __isCFrame = true }, CF)
end
function CFrame.Angles(x, y, z)
    if not (finite(x) and finite(y) and finite(z)) then fail("CFrame.Angles with a bad number") end
    return CFrame.new(0, 0, 0)
end
function CFrame.lookAt(at, target)
    if not (at and at.__isVector3 and target and target.__isVector3) then fail("CFrame.lookAt needs two Vector3s") end
    return CFrame.new(at)
end

-- Color3, UDim2, UDim ----------------------------------------------------
local Color3 = {}
function Color3.new(r, g, b) return { __isColor3 = true, r = r, g = g, b = b } end
function Color3.fromRGB(r, g, b)
    for _, c in ipairs({ r, g, b }) do
        if type(c) ~= "number" or c < 0 or c > 255 then fail("Color3.fromRGB out of range: " .. tostring(c)) end
    end
    return Color3.new(r / 255, g / 255, b / 255)
end
local UDim2 = { new = function(a, b, c, d) return { __isUDim2 = true, a, b, c, d } end }
local UDim = { new = function(a, b) return { __isUDim = true, a, b } end }

-- Enum --------------------------------------------------------------------
local PART_MATERIALS = { "Plastic", "SmoothPlastic", "Neon", "Wood", "WoodPlanks", "Marble", "Slate",
    "Concrete", "Granite", "Brick", "Pebble", "Cobblestone", "CorrodedMetal", "DiamondPlate", "Foil",
    "Metal", "Grass", "Sand", "Fabric", "Ice", "Glass", "ForceField", "Asphalt", "Basalt", "CrackedLava",
    "Glacier", "Ground", "LeafyGrass", "Limestone", "Mud", "Pavement", "Rock", "Salt", "Sandstone", "Snow" }
local TERRAIN_MATERIALS = { "Air", "Water", "Grass", "Slate", "Concrete", "Brick", "Sand", "WoodPlanks",
    "Rock", "Glacier", "Snow", "Sandstone", "Mud", "Basalt", "Ground", "CrackedLava", "Asphalt",
    "LeafyGrass", "Salt", "Limestone", "Pavement", "Ice" }
local ENUMS = {
    Material = {}, SurfaceType = { Smooth = true, Studs = true }, PartType = { Ball = true, Block = true, Cylinder = true },
    Font = { Gotham = true, GothamBold = true, GothamMedium = true, SourceSans = true, SourceSansBold = true, Arial = true },
    TextXAlignment = { Left = true, Center = true, Right = true },
}
for _, m in ipairs(PART_MATERIALS) do ENUMS.Material[m] = true end
for _, m in ipairs(TERRAIN_MATERIALS) do ENUMS.Material[m] = true end
local partMaterial, terrainMaterial = {}, {}
for _, m in ipairs(PART_MATERIALS) do partMaterial[m] = true end
for _, m in ipairs(TERRAIN_MATERIALS) do terrainMaterial[m] = true end

local Enum = setmetatable({}, { __index = function(_, category)
    local names = ENUMS[category]
    if not names then fail("no such Enum: Enum." .. tostring(category)); names = {} end
    return setmetatable({}, { __index = function(_, name)
        if not names[name] then fail("no such Enum." .. category .. "." .. tostring(name)) end
        return { __isEnum = true, category = category, name = name }
    end })
end })

-- Instances ---------------------------------------------------------------
local COMMON = { Name = true, Parent = true, Archivable = true }
local PART = { Anchored = true, Size = true, CFrame = true, Position = true, Color = true, Material = true,
    TopSurface = true, BottomSurface = true, Transparency = true, CanCollide = true, Reflectance = true,
    CastShadow = true }
local function with(base, extra) local t = {}; for k in pairs(COMMON) do t[k] = true end; for k in pairs(base) do t[k] = true end; for k in pairs(extra or {}) do t[k] = true end; return t end
local PROPS = {
    Part = with(PART, { Shape = true }),
    WedgePart = with(PART),
    SpawnLocation = with(PART, { Neutral = true, Duration = true, Enabled = true }),
    Folder = with({}),
    Model = with({}),
    BillboardGui = with({ Size = true, StudsOffsetWorldSpace = true, StudsOffset = true, AlwaysOnTop = true, MaxDistance = true, Adornee = true }),
    ScreenGui = with({ ResetOnSpawn = true, IgnoreGuiInset = true }),
    Frame = with({ Size = true, Position = true, BackgroundColor3 = true, BackgroundTransparency = true, BorderSizePixel = true }),
    TextLabel = with({ Size = true, Position = true, BackgroundColor3 = true, BackgroundTransparency = true, BorderSizePixel = true,
        Text = true, TextColor3 = true, TextStrokeTransparency = true, Font = true, TextScaled = true, TextSize = true, TextXAlignment = true }),
    UICorner = with({ CornerRadius = true }),
    Atmosphere = with({ Density = true, Haze = true, Color = true, Decay = true, Glare = true, Offset = true }),
    Lighting = with({ ClockTime = true, Brightness = true, Ambient = true, OutdoorAmbient = true, GlobalShadows = true,
        EnvironmentDiffuseScale = true, EnvironmentSpecularScale = true, FogEnd = true, FogStart = true }),
    Terrain = with({ WaterColor = true, WaterTransparency = true, WaterWaveSize = true, WaterWaveSpeed = true, WaterReflectance = true }),
    Workspace = with({}), ReplicatedStorage = with({}), Players = with({ LocalPlayer = true }), Player = with({ Character = true }), PlayerGui = with({}),
    StarterPlayer = with({}), ServerScriptService = with({}),
}

local Instance = {}
local allInstances = {}
local function newInstance(class)
    if not PROPS[class] then fail("Instance.new of a class the checker does not know: " .. tostring(class)) end
    local self = { __class = class, __props = { Name = class }, __children = {}, __attrs = {} }
    local methods = {}
    function methods.GetChildren() local c = {}; for _, ch in ipairs(self.__children) do table.insert(c, ch) end; return c end
    function methods.FindFirstChild(_, name) for _, ch in ipairs(self.__children) do if ch.Name == name then return ch end end; return nil end
    function methods.WaitForChild(_, name)
        local ch = methods.FindFirstChild(nil, name)
        if not ch then error("WaitForChild would wait forever for " .. tostring(name) .. " under " .. self.__props.Name) end
        return ch
    end
    function methods.FindFirstChildOfClass(_, cls) for _, ch in ipairs(self.__children) do if ch.ClassName == cls then return ch end end; return nil end
    function methods.IsA(_, cls) return class == cls end
    function methods.Destroy()
        local parent = self.__props.Parent
        if parent then
            for i, ch in ipairs(parent.__raw.__children) do if ch == proxy then table.remove(parent.__raw.__children, i); break end end
        end
        self.__props.Parent = nil
    end
    function methods.SetAttribute(_, k, v)
        local t = type(v)
        if t ~= "string" and t ~= "number" and t ~= "boolean" then fail("SetAttribute " .. k .. " with a " .. t) end
        self.__attrs[k] = v
    end
    function methods.GetAttribute(_, k) return self.__attrs[k] end
    function methods.Raycast(_, origin, direction)
        return { Position = Vector3.new(origin.X, 0, origin.Z), Instance = nil }
    end
    function methods.FillBlock(_, cf, size, material)
        if not (cf and cf.__isCFrame) then fail("FillBlock: first argument is not a CFrame") end
        if not (size and size.__isVector3) then fail("FillBlock: second argument is not a Vector3") end
        if not (material and material.__isEnum and terrainMaterial[material.name]) then fail("FillBlock: not a terrain material: " .. tostring(material and material.name)) end
        if size.X <= 0 or size.Y <= 0 or size.Z <= 0 then fail(string.format("FillBlock with a size that is not positive: %s", tostring(size))) end
        checks.terrainVolume = checks.terrainVolume + size.X * size.Y * size.Z
        checks.fills = checks.fills + 1
    end
    function methods.FillBall(_, centre, radius, material)
        if not (centre and centre.__isVector3) then fail("FillBall: centre is not a Vector3") end
        if not finite(radius) or radius <= 0 then fail("FillBall: bad radius") end
        if not (material and material.__isEnum and terrainMaterial[material.name]) then fail("FillBall: not a terrain material") end
        checks.terrainVolume = checks.terrainVolume + 4 / 3 * math.pi * radius ^ 3
        checks.fills = checks.fills + 1
    end
    function methods.Clear() end
    function methods.GetService(_, name)
        local s = methods.FindFirstChild(nil, name)
        if not s then error("GetService: no such service " .. tostring(name)) end
        return s
    end

    local proxy
    proxy = setmetatable({}, {
        __index = function(_, k)
            if k == "ClassName" then return class end
            if k == "__raw" then return self end
            if methods[k] then return methods[k] end
            if self.__props[k] ~= nil then return self.__props[k] end
            local ch = methods.FindFirstChild(nil, k)
            if ch then return ch end
            if PROPS[class][k] then return nil end
            error("reading " .. class .. "." .. tostring(k) .. " which is not a property or a child of it")
        end,
        __newindex = function(_, k, v)
            if not PROPS[class][k] then error("setting " .. class .. "." .. tostring(k) .. ", which is not a property it has") end
            if k == "Parent" then
                local old = self.__props.Parent
                if old then for i, ch in ipairs(old.__raw.__children) do if ch == proxy then table.remove(old.__raw.__children, i); break end end end
                if v then table.insert(v.__raw.__children, proxy) end
            elseif k == "Size" and (class == "Part" or class == "WedgePart" or class == "SpawnLocation") then
                if not (v and v.__isVector3) then error("Size must be a Vector3") end
                for _, axis in ipairs({ "X", "Y", "Z" }) do
                    if v[axis] <= 0 then fail(class .. " with a size of " .. tostring(v) .. " (" .. axis .. " is not positive)") end
                    if v[axis] > 2048 then fail(class .. " with a size of " .. tostring(v) .. " (" .. axis .. " is over 2048, Roblox will clamp it)") end
                end
            elseif k == "CFrame" then
                if not (v and v.__isCFrame) then error("CFrame must be a CFrame") end
            elseif k == "Material" then
                if not (v and v.__isEnum and v.category == "Material") then error("Material must be an Enum.Material") end
                if class ~= "Terrain" and not partMaterial[v.name] then fail(class .. " with a terrain-only material: " .. v.name) end
            elseif k == "Color" or k == "TextColor3" or k == "BackgroundColor3" or k == "WaterColor" then
                if not (v and v.__isColor3) then error(k .. " must be a Color3") end
            elseif k == "Shape" then
                if not (v and v.__isEnum and v.category == "PartType") then error("Shape must be an Enum.PartType") end
            elseif k == "Text" then
                if type(v) ~= "string" then error("Text must be a string, got " .. type(v)) end
            end
            self.__props[k] = v
        end,
    })
    if class == "Part" or class == "WedgePart" or class == "SpawnLocation" then checks.parts = checks.parts + 1 end
    table.insert(allInstances, proxy)
    return proxy
end
Instance.new = newInstance

-- The world ---------------------------------------------------------------
local game = newInstance("Folder"); game.Name = "game"
local workspace = newInstance("Workspace"); workspace.Name = "Workspace"; workspace.Parent = game
local terrain = newInstance("Terrain"); terrain.Name = "Terrain"; terrain.Parent = workspace
local baseplate = newInstance("Part"); baseplate.Name = "Baseplate"; baseplate.Parent = workspace
checks.parts = 0
for _, svc in ipairs({ "Lighting", "ReplicatedStorage", "Players", "StarterPlayer", "ServerScriptService" }) do
    local s = newInstance(svc); s.Name = svc; s.Parent = game
end

-- Luau has math.atan2 and plain Lua 5.4 does not; the scripts are Luau.
local luauMath = setmetatable({ atan2 = math.atan2 or function(y, x) return math.atan(y, x) end }, { __index = math })

-- Random, task, os ---------------------------------------------------------
local Random = {}
function Random.new(seed)
    math.randomseed(seed or 0)
    local r = {}
    function r.NextNumber(_, a, b)
        if a == nil then return math.random() end
        if a > b then fail(string.format("NextNumber(%g, %g): min is bigger than max", a, b)) end
        return a + math.random() * (b - a)
    end
    function r.NextInteger(_, a, b)
        if a > b then fail(string.format("NextInteger(%g, %g): min is bigger than max", a, b)) end
        return math.random(a, b)
    end
    return r
end
local waits = 0
local task = { wait = function()
    waits = waits + 1
    if checks.onWait then checks.onWait(waits) end
    return 0
end }

return {
    env = { Vector3 = Vector3, CFrame = CFrame, Color3 = Color3, UDim2 = UDim2, UDim = UDim, Enum = Enum,
        Instance = Instance, game = game, workspace = workspace, Random = Random, task = task, os = os,
        math = luauMath, string = string, table = table, ipairs = ipairs, pairs = pairs, print = print,
        tostring = tostring, tonumber = tonumber, type = type, setmetatable = setmetatable, error = error,
        pcall = pcall, select = select, unpack = unpack or table.unpack },
    checks = checks, instances = allInstances, game = game,
}
"""


def run(lua, source, env, name):
    load = lua.eval("function(src, env, name) local f, e = load(src, name, 't', env); return {f, e} end")
    r = load(source, env, name)
    if r[1] is None:
        return f"{name} will not even compile: {r[2]}"
    r = lua.eval("function(f) local ok, e = pcall(f); return {ok, e} end")(r[1])
    if not r[1]:
        return f"{name} crashed: {r[2]}"
    return None


def count_by_folder(mock):
    out = {}
    for inst in list(mock.instances.values()):
        if inst.ClassName in ("Part", "WedgePart") and inst.Parent is not None:
            p = inst.Parent
            name = p.Name if p is not None else "(no parent)"
            out[name] = out.get(name, 0) + 1
    return out


def main():
    lua = LuaRuntime(unpack_returned_tuples=True)
    problems = []

    # --- the server script ------------------------------------------------
    mock = lua.execute(MOCK)
    mock.env["script"] = None
    err = run(lua, SERVER.read_text(), mock.env, "BuildNewYork")
    if err:
        problems.append(err)
    for e in list(mock.checks.errors.values()):
        problems.append("BuildNewYork: " + e)
    print(f"BuildNewYork made {mock.checks.parts} parts and {mock.checks.fills} terrain fills "
          f"({mock.checks.terrainVolume / 64 / 1e6:.1f} million voxels)")
    for folder, n in sorted(count_by_folder(mock).items(), key=lambda kv: -kv[1]):
        print(f"  {n:6d}  {folder}")

    info = mock.game.ReplicatedStorage.FindFirstChild(None, "NewYorkInfo")
    if info is None:
        problems.append("BuildNewYork: never put NewYorkInfo in ReplicatedStorage, so the client would wait forever")
    spawn = None
    for ch in mock.game.Workspace.GetChildren().values():
        if ch.ClassName == "SpawnLocation":
            spawn = ch
    if spawn is None:
        problems.append("BuildNewYork: no SpawnLocation, players would fall into the sea")

    # --- the client script, with the server's info still there ------------
    if info is not None:
        players = mock.game.Players
        player = mock.env["Instance"].new("Player"); player.Name = "Alan"; player.Parent = players
        players.LocalPlayer = player
        gui = mock.env["Instance"].new("PlayerGui"); gui.Name = "PlayerGui"; gui.Parent = player
        character = mock.env["Instance"].new("Model"); character.Name = "Alan"
        root = mock.env["Instance"].new("Part"); root.Name = "HumanoidRootPart"; root.Parent = character
        player.Character = character

        V3 = mock.env["Vector3"]
        AVE, SU = 70, 27
        spots = [
            ("5th Ave & 34th", V3.new(7 * AVE, 3, -34 * SU)),
            ("Times Square", V3.new(9 * AVE, 3, -42 * SU)),
            ("inside Central Park", V3.new(8.5 * AVE, 3, -80 * SU)),
            ("Upper West Side", V3.new(12 * AVE, 3, -80 * SU)),
            ("Wall Street", V3.new(7 * AVE, 3, 15 * SU)),
            ("in the Hudson", V3.new(17 * AVE, 3, -50 * SU)),
            ("in the East River", V3.new(-2 * AVE, 3, -50 * SU)),
            ("Brooklyn", V3.new(-8 * AVE, 3, 10 * SU)),
            ("the harbour", V3.new(7 * AVE, 3, 60 * SU)),
            ("past the border", V3.new(40 * AVE, 3, -50 * SU)),
        ]
        results = []

        def on_wait(_):
            n = len(results) + 1
            labels = [i for i in mock.instances.values() if i.ClassName == "TextLabel" and i.Parent is not None and i.Parent.ClassName == "Frame"]
            texts = [str(l.Text) for l in labels]
            results.append(" / ".join(texts))
            if n >= len(spots):
                raise Exception("STOP")
            root.Position = spots[n][1]

        root.Position = spots[0][1]
        mock.checks.onWait = on_wait
        err = run(lua, CLIENT.read_text(), mock.env, "Neighbourhood")
        if err and "STOP" not in err:
            problems.append(err)

        for e in list(mock.checks.errors.values()):
            if "BuildNewYork" not in e:
                problems.append("Neighbourhood: " + e)
        print("\nNeighbourhood says:")
        for (name, _), text in zip(spots, results):
            print(f"  standing {name:22s} -> {text}")
        if len(results) != len(spots):
            problems.append("Neighbourhood: did not get through all the test spots")

    print()
    if problems:
        seen = set()
        for p in problems:
            if p not in seen:
                seen.add(p)
                print("PROBLEM:", p)
        sys.exit(1)
    print("No problems found. (Only Studio can tell you if it looks right.)")


if __name__ == "__main__":
    main()
