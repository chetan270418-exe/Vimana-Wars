$ErrorActionPreference = "Stop"

# Always run from the web project, even when this script is launched from the
# repository root or by double-clicking it in Explorer.
Set-Location $PSScriptRoot

# Figma's pnpm install creates a valid node_modules tree, but npm 11 can try
# to re-read pnpm's internal package links and report a false `workspace:*`
# protocol error. Reuse the ready tree instead of reinstalling it.
$viteBinary = Join-Path $PSScriptRoot "node_modules\.bin\vite.cmd"
if (Test-Path $viteBinary) {
    Write-Host "Web dependencies are already installed; starting Vite."
    npm run dev
    exit $LASTEXITCODE
}

if (Get-Command pnpm -ErrorAction SilentlyContinue) {
    pnpm install --frozen-lockfile
    if ($LASTEXITCODE -eq 0) {
        pnpm run dev
        exit $LASTEXITCODE
    }
    Write-Warning "pnpm install failed; trying Corepack/npm fallback."
}

if (Get-Command corepack -ErrorAction SilentlyContinue) {
    Write-Host "pnpm was not found; using Corepack to provide pnpm."
    corepack pnpm install --frozen-lockfile
    if ($LASTEXITCODE -eq 0) {
        corepack pnpm run dev
        exit $LASTEXITCODE
    }
    Write-Warning "Corepack pnpm install failed; trying npm fallback."
}

if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "pnpm/Corepack was not found; using npm instead."
    npm install --no-package-lock
    if ($LASTEXITCODE -ne 0) {
        Write-Error "npm could not install the web dependencies. Install pnpm or enable Corepack, then run this script again."
    }
    npm run dev
    exit $LASTEXITCODE
}

Write-Error "Neither pnpm nor npm is installed. Install Node.js from https://nodejs.org/ and run this script again."
