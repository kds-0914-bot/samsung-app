# Azure 배포 자동화 스크립트
# PowerShell 관리자로 실행

param(
    [string]$resourceGroup = "samsung-rg",
    [string]$registryName = "samsungapp",
    [string]$containerName = "samsung-app-instance",
    [string]$imageName = "samsung-app:latest"
)

Write-Host "🚀 Azure 배포 시작..." -ForegroundColor Green

# Step 1: Docker 이미지 빌드
Write-Host "`n1️⃣  Docker 이미지 빌드 중..." -ForegroundColor Cyan
docker build -t $imageName .

# Step 2: ACR 로그인
Write-Host "`n2️⃣  Azure Container Registry 로그인..." -ForegroundColor Cyan
az acr login --name $registryName

# Step 3: 이미지 태그 지정
Write-Host "`n3️⃣  이미지 태그 지정 중..." -ForegroundColor Cyan
$acrUrl = "$registryName.azurecr.io"
docker tag $imageName "$acrUrl/$imageName"

# Step 4: 이미지 Push
Write-Host "`n4️⃣  이미지를 레지스트리에 Push 중..." -ForegroundColor Cyan
docker push "$acrUrl/$imageName"

# Step 5: 자격증명 확인
Write-Host "`n5️⃣  ACR 자격증명 확인..." -ForegroundColor Cyan
$credentials = az acr credential show --name $registryName | ConvertFrom-Json
$username = $credentials.username
$password = $credentials.passwords[0].value

# Step 6: Container 배포
Write-Host "`n6️⃣  Azure Container에 배포 중..." -ForegroundColor Cyan
az container create `
  --resource-group $resourceGroup `
  --name $containerName `
  --image "$acrUrl/$imageName" `
  --registry-login-server $acrUrl `
  --registry-username $username `
  --registry-password $password `
  --cpu 1 `
  --memory 1 `
  --ports 5000 `
  --protocol TCP

# Step 7: 배포 완료 정보 출력
Write-Host "`n✅ 배포 완료!" -ForegroundColor Green
Write-Host "`n📍 배포된 앱 확인:" -ForegroundColor Yellow
az container show --resource-group $resourceGroup --name $containerName --query "[publicIps[0].ip, ports[0].port]" -o table

Write-Host "`n💡 팁: 아래 URL로 접속하세요:"
$ip = az container show --resource-group $resourceGroup --name $containerName --query "publicIps[0].ip" -o tsv
Write-Host "http://$ip:5000" -ForegroundColor Cyan
