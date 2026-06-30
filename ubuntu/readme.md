## doker desktop 설치 및 실행
## 필수 유틸리티설치
1. 관리자 권한으로 powershell 실행
2. WSL 기능 및 가상 멋니 플랫폼 활성화
```
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
3. WSL 최신 커널 업데이트 설치 및 재부팅
```
wsl --install
```
4. 설치 검증
```
docker --version
```