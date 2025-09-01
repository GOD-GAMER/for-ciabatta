# Port Forwarding & Windows Firewall

This guide helps you expose your BakeBot leaderboard to the internet.

## Default Ports
- Web/Leaderboard: TCP 8080 (WEB_PORT)
- EventSub (optional): TCP 8081 (EVENTSUB_PORT)

## Find Your Local IPv4
- Open the GUI ? Network tab, or run `ipconfig` and note IPv4 Address.

## Router: Create Port Forwards
- Forward 8080 TCP external ? your PC’s Local IPv4, port 8080
- (Optional) Forward 8081 TCP for EventSub
- Save/apply and test from mobile data: `http://YOUR_PUBLIC_IP:8080/leaderboard`

Router quick paths
- TP?Link Archer (new): Advanced ? NAT Forwarding ? Virtual Servers ? Add New
- Netgear Nighthawk: Advanced ? Advanced Setup ? Port Forwarding/Port Triggering ? Add Custom Service
- ASUSWRT: WAN ? Virtual Server / Port Forwarding ? Add
- Linksys Smart Wi?Fi: Security ? Apps and Gaming ? Single Port Forwarding
- UniFi/Dream Machine: Settings ? Security & Gateway ? Port Forwarding ? Create Rule
- Xfinity xFi: xFi app ? Network ? Advanced Settings ? Port Forwarding
- Verizon Fios: Advanced ? Security ? Port Forwarding ? Add Rule
- AT&T BGW210/320: Firewall ? NAT/Gaming ? Custom Service ? Add
- Spectrum: App or router UI ? Advanced ? Port Forwarding
- BT Smart Hub 2: Advanced Settings ? Port Forwarding ? Add
- Virgin Media Hub: Advanced Settings ? Security ? Port Forwarding ? Create Rule

Notes
- If the UI asks for External and Internal ports, set both to 8080 (or your chosen WEB_PORT)
- Create a DHCP reservation (Static Lease) so your PC’s IP doesn’t change
- If your WAN IP is 100.64.x.x, you’re behind CGNAT ? use a tunnel (see WEB.md)

## Windows Firewall (PowerShell)
Run PowerShell as Administrator.

Allow ports
```
New-NetFirewallRule -DisplayName "BakeBot Web 8080" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8080
New-NetFirewallRule -DisplayName "BakeBot EventSub 8081" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8081
```

Allow python.exe (optional)
```
$py = (Get-Command python).Source
New-NetFirewallRule -DisplayName "BakeBot Python" -Direction Inbound -Action Allow -Program $py
```

Inspect
```
Get-NetFirewallRule | Where-Object DisplayName -like "*BakeBot*" | Format-Table -AutoSize
Get-NetTCPConnection -State Listen | Where-Object LocalPort -in 8080,8081 | Format-Table -AutoSize
netstat -ano | findstr ":8080"
```

Remove
```
Remove-NetFirewallRule -DisplayName "BakeBot Web 8080"
Remove-NetFirewallRule -DisplayName "BakeBot EventSub 8081"
```

Troubleshooting
- Double NAT: forward on both routers, or bridge one
- ISP modem/router: enable Bridge/Pass-through mode
- Port in use: change WEB_PORT and update router
- Use an online checker (canyouseeme.org) with the port number
