local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local CoreGui = game:GetService("CoreGui")

local ScreenGui = Instance.new("ScreenGui")
local MainFrame = Instance.new("Frame")
local UICorner = Instance.new("UICorner")
local Title = Instance.new("TextLabel")
local Subtitle = Instance.new("TextLabel")
local Shadow = Instance.new("ImageLabel")

ScreenGui.Name = "ExportLoadingScreen"
ScreenGui.Parent = CoreGui
ScreenGui.ResetOnSpawn = false

MainFrame.Name = "MainFrame"
MainFrame.Size = UDim2.new(0, 400, 0, 150)
MainFrame.Position = UDim2.new(0.5, -200, 0.5, -75)
MainFrame.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
MainFrame.BackgroundTransparency = 1
MainFrame.BorderSizePixel = 0
MainFrame.Parent = ScreenGui

Shadow.Name = "Shadow"
Shadow.Image = "rbxassetid://1316045217"
Shadow.ImageColor3 = Color3.fromRGB(0, 0, 0)
Shadow.ImageTransparency = 1
Shadow.ScaleType = Enum.ScaleType.Slice
Shadow.SliceCenter = Rect.new(10, 10, 118, 118)
Shadow.Size = UDim2.new(1, 20, 1, 20)
Shadow.Position = UDim2.new(0, -10, 0, -10)
Shadow.BackgroundTransparency = 1
Shadow.Parent = MainFrame

UICorner.CornerRadius = UDim.new(0, 14)
UICorner.Parent = MainFrame

Title.Size = UDim2.new(1, 0, 0, 60)
Title.Position = UDim2.new(0, 0, 0.1, 0)
Title.BackgroundTransparency = 1
Title.Text = "Exporting Models..."
Title.TextColor3 = Color3.fromRGB(240, 240, 240)
Title.Font = Enum.Font.GothamSemibold
Title.TextSize = 22
Title.TextTransparency = 1
Title.Parent = MainFrame

Subtitle.Size = UDim2.new(1, 0, 0, 30)
Subtitle.Position = UDim2.new(0, 0, 0.5, 0)
Subtitle.BackgroundTransparency = 1
Subtitle.Text = "Please wait, game may freeze temporarily."
Subtitle.TextColor3 = Color3.fromRGB(180, 180, 180)
Subtitle.Font = Enum.Font.Gotham
Subtitle.TextSize = 14
Subtitle.TextTransparency = 1
Subtitle.Parent = MainFrame

local isExporting = false

local function toggleLoadingScreen(show)
    local info = TweenInfo.new(0.5, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
    local targetTransparency = show and 0 or 1
    local frameTarget = show and 0.15 or 1
    local shadowTarget = show and 0.8 or 1

    TweenService:Create(MainFrame, info, {BackgroundTransparency = frameTarget}):Play()
    TweenService:Create(Shadow, info, {ImageTransparency = shadowTarget}):Play()
    TweenService:Create(Title, info, {TextTransparency = targetTransparency}):Play()
    TweenService:Create(Subtitle, info, {TextTransparency = targetTransparency}):Play()
end

local function exportModels()
    if isExporting then return end
    isExporting = true

    Title.Text = "Exporting Models..."
    Subtitle.Text = "Please wait, game may freeze temporarily."
    toggleLoadingScreen(true)

    task.wait(0.6) 

    local success, err = pcall(function()
        if saveinstance then
            saveinstance({
                mode = "optimized",
                noscripts = true,
                isolate = true
            })
        else
            error("saveinstance not supported")
        end
    end)

    if success then
        Title.Text = "Export Complete!"
        Subtitle.Text = "Check your executor's 'workspace' folder."
    else
        Title.Text = "Export Failed"
        Subtitle.Text = "Your executor does not support saveinstance()."
    end

    task.wait(3.5)
    toggleLoadingScreen(false)
    task.wait(0.6) 
    
    isExporting = false
end

UserInputService.InputBegan:Connect(function(input, processed)
    if processed then return end
    if input.KeyCode == Enum.KeyCode.Z then
        exportModels()
    end
end)
