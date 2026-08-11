# MST400 — Microsoft Cloud Administration
## Comprehensive Final Exam Study Guide

**Exam:** Thursday, August 13 · In person, Room C2032
**Format:** Closed book · 29 questions · Multiple choice + short answer · 80 minutes
**Pace:** ~2.75 min/question. Do every MC question first, then spend leftover time on short answers.

Built from all 11 lecture modules (Dr. Hooshang Kazemi) and Labs 01–08.

---

## Table of Contents

1. [The 60-Second Cram Sheet (numbers that get tested)](#1-the-60-second-cram-sheet)
2. [Module 1 — Users, Groups & Identities](#2-module-1--users-groups--identities)
3. [Module 2 — Governance: Regions, Subscriptions, Cost, Tags, RBAC](#3-module-2--governance-regions-subscriptions-cost-tags-rbac)
4. [Module 3 — Azure Administration: ARM, Resource Groups, Tools, Templates](#4-module-3--azure-administration-arm-resource-groups-tools-templates)
5. [Module 4 — Virtual Networking: VNets, NSGs, Firewall, DNS](#5-module-4--virtual-networking-vnets-nsgs-firewall-dns)
6. [Module 5 — Intersite Connectivity: Peering, VPN, ExpressRoute](#6-module-5--intersite-connectivity-peering-vpn-expressroute)
7. [Module 6 — Traffic Management: Load Balancer, App Gateway, Routing](#7-module-6--traffic-management-load-balancer-app-gateway-routing)
8. [Module 7 — Azure Storage](#8-module-7--azure-storage)
9. [Module 8 — Virtual Machines](#9-module-8--virtual-machines)
10. [Module 9 — App Service & Containers](#10-module-9--app-service--containers)
11. [Module 10 — Data Protection: Backup & Site Recovery](#11-module-10--data-protection-backup--site-recovery)
12. [Module 11 — Monitoring: Azure Monitor, Alerts, Log Analytics, Network Watcher](#12-module-11--monitoring-azure-monitor-alerts-log-analytics-network-watcher)
13. [Lab Recap 01–08 (what you did and why it matters)](#13-lab-recap-0108)
14. [Master Comparison Tables ("which one do I pick?")](#14-master-comparison-tables)
15. [PowerShell / CLI Command Sheet](#15-powershell--cli-command-sheet)
16. [Practice Exam — 45 MC questions with answers](#16-practice-exam--multiple-choice)
17. [Practice Short-Answer Questions with model answers](#17-practice-short-answer-questions)
18. [Night-Before Checklist & Exam Strategy](#18-night-before-checklist--exam-strategy)

---

## 1. The 60-Second Cram Sheet

These are the exact numbers and hard facts most likely to appear as multiple choice. **If you memorize nothing else, memorize this table.**

### Numbers

| Value | What it is |
|---|---|
| **5** | IP addresses Azure reserves in **every subnet** (x.0 network, x.1 gateway, x.2 & x.3 DNS, x.255 broadcast) |
| **50** | Max tag name/value pairs per resource or resource group |
| **50 → 500** | Default VNets per subscription per region → max by contacting Azure support |
| **65001** | Priority of the default `AllowInternetOutbound` NSG rule (cannot be deleted) |
| **100–4096** | Valid custom NSG rule priority range (lower number = **higher** priority / evaluated first) |
| **100** | Max public IP addresses associable with Azure Firewall |
| **/27 or /28** | Recommended size for the **GatewaySubnet** (VPN gateway) |
| **/27 or larger** | Required dedicated subnet size for **Application Gateway** |
| **90 days** | Azure **Activity Log** retention |
| **14 days** | Backup **soft delete** retention after deletion |
| **2 days** | Default instant-restore snapshot retention (configurable **1–5 days**) |
| **32 TB** | Max disk size supported by VM backup snapshots |
| **30 days** | Minimum storage duration for **Cool** blob tier |
| **180 days** | Minimum storage duration for **Archive** blob tier |
| **8 TB** | Max size of a **page blob** |
| **256-bit AES** | Storage Service Encryption (SSE) — always on, cannot be disabled |
| **5 GB** | Cloud Shell `$HOME` persistent image size (in your Azure File share) |
| **3 / 6** | Replicas: LRS & ZRS = 3 · GRS & GZRS = 6 |
| **5 → 20** | Default update domains (non-configurable at 5 by default) → max configurable |
| **3** | Minimum availability zones in any AZ-enabled region |
| **35 TB** | Max capacity of an Azure Data Box Disk shipment (1–5 disks) |
| **10 GB** | Max App Service backup size (app + database) |
| **5** | Max action groups attachable to a single alert rule |
| **3x/day** | Max MARS agent backup frequency |

### SLA numbers (very commonly tested)

| Configuration | SLA |
|---|---|
| 2+ VMs across 2+ **Availability Zones** | **99.99%** |
| 2+ VMs in an **Availability Set** | **99.95%** |
| **Single VM** using premium storage | **99.9%** |
| Enterprise Agreement subscription | 99.95% monthly |

### App Service deployment slots by tier

| Tier | Slots |
|---|---|
| Free, Shared, Basic | **0** |
| Standard | up to **5** |
| Premium | up to **20** |
| Isolated | up to **20** |

### One-liners that are almost certainly on the exam

- **Tags are NOT inherited** — a tag on a resource group does not flow to resources inside it.
- **Resource groups cannot be renamed.** A resource lives in exactly **one** resource group.
- A resource group **can** span regions and resource types.
- **Locks ARE inherited** by child resources. Two types: **ReadOnly** and **Delete (CanNotDelete)**.
- Only **Owner** and **User Access Administrator** can create/delete management locks.
- **VNet peering is non-transitive.** A↔B and B↔C does *not* give you A↔C.
- Peered VNet address spaces **must not overlap**.
- The VPN gateway subnet **must be named exactly `GatewaySubnet`** — never put other resources in it.
- **Azure Firewall denies all traffic by default.** Rule order: **NAT → Network → Application**.
- **NSG:** a subnet can have **0 or 1** NSG; a NIC can have **0 or 1** NSG. One NSG can be associated many times.
- **NSG evaluation:** inbound = **subnet first, then NIC**; outbound = **NIC first, then subnet**. An **allow rule must exist at both levels**.
- A subnet can be associated with **only one route table**; a route table can serve **many subnets**. Route tables are **free**.
- **Blob type cannot be changed** after creation. **Access tier can** be changed any time.
- **Load Balancer = Layer 4.** **Application Gateway = Layer 7** (WAF, SSL termination, URL path routing).
- **Activity Log is a subscription-level log**, kept 90 days.
- Custom domain verification in Entra ID uses an **MX or TXT** DNS record.
- Mapping a custom domain to a web app uses a **CNAME or A** record.

---

## 2. Module 1 — Users, Groups & Identities

### Why an identity provider?
Traditional per-application authentication means security risks, duplicated security features, time-consuming procedures, and **unique credentials for every application**. An identity provider (Microsoft Entra ID) centralizes this.

**Benefits of an identity provider:**
- Centralized management
- Lower risk via extra features: MFA, Conditional Access, etc.

### Microsoft Entra ID vs. Windows Server Active Directory (AD DS)

This comparison is a near-guaranteed short-answer question.

| | **Microsoft Entra ID** | **Windows Server AD DS** |
|---|---|---|
| Purpose | Primarily an **identity** solution (cloud) | Full directory service (on-prem) |
| Query protocol | **REST API over HTTP/HTTPS** | **LDAP** |
| Auth protocols | **SAML, WS-Federation, OpenID Connect** (OAuth for *authorization*) | **Kerberos / NTLM** |
| Structure | **Flat** — no OUs, no GPOs | Hierarchical — OUs, GPOs, forests, domains, trees |
| Federation | Includes federation services and third-party services (e.g. Facebook) | Requires AD FS |
| Devices | Entra join / registration | Domain join |

> **Remember the phrase:** *"Entra ID users and groups are created in a flat structure — there are no Organizational Units (OUs) or Group Policy Objects (GPOs)."*

**Entra ID lets you:**
- Configure access to applications, including **single sign-on (SSO)**
- Manage and provision users and groups
- Provide an identity management solution, including **federation**
- Implement **MFA** and **Conditional Access**

### Core concepts (memorize these definitions)

| Concept | Definition |
|---|---|
| **Identity** | An object that **can be authenticated** |
| **Account** | An identity that **has data associated with it** |
| **Entra ID account** | An identity created through Entra ID or another Microsoft cloud service |
| **Tenant / Directory** | A **dedicated, trusted instance** of Entra ID representing **a single organization**. Automatically created when your org signs up for a Microsoft cloud subscription. Terms *tenant* and *directory* are used interchangeably. Additional instances can be created. |
| **Azure subscription** | Used to **pay for** Azure cloud services — a logical container for provisioning/managing resources; a unit of **management, billing, and scale** |

**Tenant vs. Subscription** (classic short-answer):
- **Tenant** = identity boundary (who you are). One organization = one default tenant, created automatically.
- **Subscription** = billing/resource boundary (what you pay for). Holds VMs, databases, etc. An organization can have **multiple** subscriptions (production, Dev/Test, sandbox) to separate environments/projects.

### Entra ID plan comparison (Free / P1 / P2)

| Feature | Free | P1 | P2 |
|---|:--:|:--:|:--:|
| Single Sign-On (unlimited) | ✔ | ✔ | ✔ |
| Cloud and federated authentication | ✔ | ✔ | ✔ |
| Self-service account management portal | ✔ | ✔ | ✔ |
| Multifactor authentication (MFA) | ✔ | ✔ | ✔ |
| Advanced group management | | ✔ | ✔ |
| Conditional Access | | ✔ | ✔ |
| Automated user/group provisioning to apps | | ✔ | ✔ |
| **Risk-based** Conditional Access (sign-in risk, user risk) | | | ✔ |
| **Privileged Identity Management (PIM)** | | | ✔ |
| Governance | | | ✔ |

> **The exam trick:** anything with **"risk-based"** or **PIM** = **P2**. Plain Conditional Access and advanced group management = **P1**. Basic SSO + MFA = Free.
> **Administrative Units** also require **P1 or P2**.

### Windows Server AD + Entra ID + Entra Domain Services
- **Microsoft Entra Connect** performs **synchronization** from Windows Server AD → Entra ID.
- **Microsoft Entra Domain Services** provides managed domain services (domain join, LDAP, Kerberos) in Azure without deploying domain controllers.

**Benefits of Entra ID + on-premises AD join:**
1. **Single Sign-On** to Entra-managed SaaS apps without extra prompts, even off the domain network
2. **Enterprise compliant roaming** of user settings across joined devices (no Microsoft account needed)
3. **Microsoft Store for Business** access with the Entra ID account
4. **Windows Hello** support
5. **Compliance policy enforcement** — restrict app access to compliant devices only
6. **Seamless on-premises resource access** when the device has line of sight to a domain controller

### Self-Service Password Reset (SSPR)
Purpose: reduce helpdesk calls by letting users reset their own passwords.

Three configuration decisions:
1. **Who** can use SSPR (none / selected group / all)
2. **How many** authentication methods are required, and **which** methods are available (email, phone, security questions)
3. Whether to **require users to register** for SSPR (same process as MFA registration)

### The three ways Entra defines users

| Type | Where they exist | Source |
|---|---|---|
| **Cloud identities** | Only in the Entra directory | Azure Active Directory / Entra ID |
| **Directory-synchronized identities** | On-premises AD, synced in via **Entra Connect** | **Windows Server AD** |
| **Guest users** | Outside Azure (other cloud providers, other accounts) | **Invited user** |

> Exam trick: they'll show a user's **Source** field and ask what kind of user it is. `Windows Server AD` → synchronized. `Invited user` → guest. `Azure Active Directory` → cloud identity.

### Group accounts

**Group types:**
- **Security groups** — manage access to resources
- **Microsoft 365 groups** — collaboration (mailbox, calendar, files); can include people outside the org

**Membership types:**
- **Assigned** — manually add specific members
- **Dynamic User** — rule-based, membership auto-updates as user attributes change
- **Dynamic Device** — rule-based on device attributes — **security groups only** (not M365 groups)

> Exam trick: *"Which membership type is NOT available for Microsoft 365 groups?"* → **Dynamic Device**.

### Administrative Units (AUs)
Delegate admin permissions over a **subset** of the directory (e.g., let a regional IT admin manage only that region's users).

Four steps:
1. Create an administrative unit
2. Populate it with users or groups
3. Create a role with appropriate permissions **scoped to the AU**
4. Add IT members to the role

**Requirements:** Entra ID **P1 or P2**, and the **Privileged Role Administrator** or **Global Administrator** role.

### PowerShell for group management

```powershell
New-AzADGroup -DisplayName Developers -MailNickname Developers   # create group
Get-AzADGroup                                                    # find the group ObjectId
Get-AzADUser                                                     # find the user ObjectId
Add-AzADGroupMember -MemberUserPrincipalName "me@domain.com" `
                    -TargetGroupDisplayName "MyGroupDisplayName" # add member
Get-AzADGroupMember -GroupDisplayName "MyGroupDisplayName"       # verify
```

---

## 3. Module 2 — Governance: Regions, Subscriptions, Cost, Tags, RBAC

### Azure Regions
- Azure is made of **datacenters around the globe**, organized and made available by **region**.
- A **region** = a geographical area containing **at least one, but potentially multiple, datacenters**.
- Each Azure region is **paired with another region within the same geography** — together a **regional pair**.

> Why regional pairs matter: planned updates roll out to only one region of a pair at a time; data residency stays within the same geography; GRS storage replicates to the paired region.

### Azure Subscriptions
An **Azure subscription** is a **logical unit of Azure services linked to an Azure account**.

**Four ways to get a subscription:**

| Method | Key detail |
|---|---|
| **Enterprise Agreement** | Upfront **monetary commitment** consumed through the year across any Azure services. **99.95% monthly SLA.** |
| **Reseller** | Buy through the **Open Licensing** program from a Microsoft reseller; activate/add credits with an "Azure in Open" license key |
| **Partners** | A Microsoft partner designs and implements your Azure solution |
| **Personal free account** | Free trial; **not charged until you choose to upgrade** |

### Cost Management
"With Azure products and services, **you only pay for what you use**."

Azure **Cost Management and Billing** features:
- **Cost analysis** — explore and analyze spend
- **Budgets** — set spending thresholds with alerts
- **Recommendations** — advice on reducing cost
- **Exporting cost management data** — push data out for reporting

### Resource Tags
- Apply tags to **logically organize resources by category**. Each tag = a **name and a value**.
- **Maximum 50 tag name/value pairs** per resource or resource group.
- **Tags applied to a resource group are NOT inherited by the resources inside it.** ← *guaranteed exam question*

Typical uses: cost center, environment (prod/dev), owner, department, project.

### RBAC and role assignments
- A **role assignment** is the process of **binding a role to a security principal at a particular scope**, for the purpose of **granting access**.
- A **resource inherits role assignments from its parent resources.**

**Scope hierarchy (top → bottom, inheritance flows down):**
```
Management Group → Subscription → Resource Group → Resource
```

**Azure RBAC roles vs. Entra ID roles:**

| | **Azure RBAC roles** | **Entra ID roles** |
|---|---|---|
| Controls access to | **Azure resources** (VMs, storage, networks) | **Entra ID resources** (users, groups, licenses, domains) |
| Scope | Management group / subscription / RG / resource | **Tenant-wide** |
| Examples | Owner, Contributor, Reader, User Access Administrator | Global Administrator, User Administrator, Billing Administrator |

**Core built-in Azure roles:**

| Role | Can do |
|---|---|
| **Owner** | Full access **+ can delegate access to others** |
| **Contributor** | Create and manage all resources, but **cannot grant access** |
| **Reader** | View resources only |
| **User Access Administrator** | Manage user access to Azure resources (permissions only) |

> Exam trick: "The user must manage all resources but must NOT be able to give other people access" → **Contributor**.

### Azure Policy (demonstration topic)
Enforces **organizational standards and compliance** — e.g., only allow certain VM SKUs, require a tag, restrict deployment regions. Policy governs **what** can be deployed; **RBAC** governs **who** can deploy.

---

## 4. Module 3 — Azure Administration: ARM, Resource Groups, Tools, Templates

### Azure Resource Manager (ARM) — the consistent management layer
All Azure tools (portal, PowerShell, CLI, SDKs, REST) call the **Azure Resource Manager API**. ARM:
1. **Authenticates and authorizes** the request
2. **Routes** the request to the appropriate **resource provider**

> This is why you get consistent behavior, RBAC, tagging, and locking no matter which tool you use.

### Terminology

| Term | Definition |
|---|---|
| **Resource** | A manageable service available through Azure (VM, storage account, web app, database, VNet) |
| **Resource group** | A **logical container** that holds related resources |
| **Resource provider** | A service that supplies the resources — e.g. `Microsoft.Compute` (VMs), `Microsoft.Storage` (storage accounts), `Microsoft.Web` (web apps) |
| **ARM template** | A **JSON** file that **declaratively** defines one or more resources to deploy to a resource group |
| **Declarative syntax** | You define the *properties of what you want* without writing programming commands to create it. The ARM template is the example. |

### Resource Group rules (high-yield)
- A resource group is a **logical container** for resources.
- **All resources in a group should share the same lifecycle** — deploy, update, delete them together.
- A resource can exist in **only one** resource group.
- Resource groups **cannot be renamed**.
- A resource group **can hold many different resource types**.
- A resource group **can hold resources from many different regions**.

### Resource Manager Locks
Purpose: **prevent accidental deletion/change** of resources.

- Can be applied at **subscription, resource group, or resource** scope.
- **Locks are inherited by child resources.**
- **Two lock types:**
  - **Read-Only** — prevents **any changes** to the resource (and blocks delete)
  - **Delete (CanNotDelete)** — prevents **deletion**, changes still allowed
- Only the **Owner** and **User Access Administrator** roles can create or delete management locks.

```powershell
New-AzResourceLock -LockName <lockName> -LockLevel CanNotDelete -ResourceGroupName <rgName>
Get-AzResourceLock                                   # note the LockId
Remove-AzResourceLock -LockName <name> -ResourceGroupName <rg>
```

### Moving resources
When you move resources, **both the source and target resource groups are locked** during the operation. Write and delete operations are blocked on both RGs until the move completes — you can't add, update, or delete resources in them. **The resources themselves remain available** (the lock does not mean downtime).

### Deleting resource groups
Remove unused resources to avoid unexpected charges.

```powershell
Get-AzResourceGroup                                                # list
Remove-AzResourceGroup -Name "<resource_Group_Name>" -Force -AsJob # delete
```

### Resource limits
- The limits shown are the limits **for your subscription**.
- When you need to increase a default limit, there is a **"Request Increase"** link.
- All resources have a **maximum limit** listed in Azure limits.
- **If you are already at the maximum limit, it cannot be increased.**

### Management tools

**Azure Portal** — search resources/services/docs, manage resources, create **customized dashboards and favorites**, access **Cloud Shell**, receive notifications, links to documentation.

**Azure Cloud Shell:**
- Interactive, **browser-accessible** shell
- **Bash** (Linux users) or **PowerShell** (Windows users)
- **Authenticates automatically** for instant access to your resources
- **Requires a resource group, a storage account, and an Azure File share**
- **Persists `$HOME` using a 5-GB image** held in your file share

**Azure PowerShell** — module name is **Az**.
```powershell
Get-Verb                                    # show approved verbs
New-AzVm -ResourceGroupName "Demo-RG" -Name "Demo-VM" -Image "UbuntuLTS"
Get-Help Get-ChildItem -detailed            # help for any cmdlet
```

**Azure CLI** — command-line program to connect to Azure and run administrative commands.
```bash
az vm restart -g MyResourceGroup -n MyVm
az find                                     # get help
```
- Runs on **Linux, macOS, and Windows**
- Can be used **interactively or through scripts**

### ARM template structure
ARM templates are written in **JSON** — data stored as objects in text. A JSON object is a **collection of key-value pairs**; each key is a string, and the value can be a **string, number, Boolean, list of values, or object**.

```json
{
  "$schema": "http://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "",
  "parameters": {},
  "variables": {},
  "functions": [],
  "resources": [],
  "outputs": {}
}
```

| Section | Purpose |
|---|---|
| `$schema` | Location of the JSON schema file describing the template language version |
| `contentVersion` | Your own version of the template |
| **`parameters`** | **Values you supply at deployment time** (e.g. VM username and password) |
| `variables` | Values reused throughout the template |
| `functions` | User-defined functions |
| **`resources`** | **The resources actually deployed** |
| `outputs` | Values returned after deployment |

**Benefits of templates:** repeatable/idempotent deployments, version control, consistency across environments, parameterization for reuse, faster than manual portal work.

> **Lab tie-in:** In Lab 01 you exported a VNet as a template from the **Automation → Export template** blade, then edited `template.json` and `parameters.json` and re-deployed with **Deploy a custom template → Build your own template in the editor → Load file**.

---

## 5. Module 4 — Virtual Networking: VNets, NSGs, Firewall, DNS

### VNet implementation types
1. **Dedicated private cloud-only VNet** — services and VMs communicate directly and securely with each other in the cloud; you can still configure endpoint connections for VMs/services needing internet.
2. **Securely extend your datacenter** — build traditional **site-to-site (S2S)** VPNs. S2S uses **IPsec** for a secure connection between your corporate VPN gateway and Azure.
3. **Enable hybrid cloud scenarios** — securely connect cloud applications to on-premises systems including mainframes and Unix systems.

### Subnets
- A VNet can be segmented into **one or more subnets** for better security and management.
- Subnets provide **logical divisions** within your network.
- Each subnet contains a **range of IP addresses that fall within the VNet address space**.
- **Every virtual network must have at least one subnet.**

### VNet design considerations
- **Service requirements** — some services **require their own subnet**, so keep enough unallocated address space.
- **Virtual appliances** — Azure routes traffic between all subnets in a VNet **by default**; you can override this default routing with a **network virtual appliance (NVA)** + UDR.
- **Service endpoints** — limit access to Azure resources in specific subnets; you can enable an endpoint for some subnets and not others.
- **Network security groups** — each NSG contains rules that allow/deny traffic; you can associate **zero or one** NSG to each subnet.

### The 5 reserved IPs per subnet ⚠️ *guaranteed exam question*

| Address | Reserved for |
|---|---|
| `x.x.x.0` | Network address |
| `x.x.x.1` | Azure **default gateway** |
| `x.x.x.2` and `x.x.x.3` | Azure — **maps Azure DNS IPs to the VNet space** |
| `x.x.x.255` | Network **broadcast** address |

> **Do the math:** a `/24` has 256 addresses → **251 usable**. A `/27` has 32 → **27 usable**. A `/29` has 8 → **3 usable**.

### VNet limits
- By default you can create up to **50 virtual networks per subscription per region**.
- This can be increased to **500** by **contacting Azure support**.

### VNet PowerShell
```powershell
$myVNet2 = New-AzVirtualNetwork -ResourceGroupName demo-RG -Location EastUS `
             -Name myVNet2 -AddressPrefix 10.0.0.0/16
Get-AzVirtualNetwork -Name myVNet2
$mySubnet2 = Add-AzVirtualNetworkSubnetConfig -Name mySubnet2 `
             -AddressPrefix 10.0.0.0/24 -VirtualNetwork $myVNet2
Get-AzVirtualNetworkSubnetConfig -Name mySubnet2 -VirtualNetwork $myVNet2
$mySubnet2 | Set-AzVirtualNetwork      # associate subnet to the VNet (commits the change)
```

### IP addressing
- IP addresses can be **statically** assigned or **dynamically (DHCP)** assigned.
- It is better to **separate dynamically and statically assigned IP resources into different subnets**.
- **IP addresses are never managed from within a virtual machine** — always configure them in Azure. (Setting a static IP inside the guest OS breaks connectivity.)
- **Private IP addresses** — used within an Azure VNet and on-premises networks when a **VPN gateway or ExpressRoute circuit** extends the local site to Azure.
- **Public IP addresses** — used for communication with the Internet, including Azure public-facing services.
- **Static public IP addresses are only available on certain SKUs** (Standard SKU public IP = static).

### Network Security Groups (NSGs)

- An NSG contains a **list of security rules that allow or deny inbound or outbound network traffic**.
- NSG rules prevent unwanted or unsecured traffic from reaching key systems.
- An NSG can be associated to a **subnet** or a **network interface (NIC)**.
- **A single NSG can be associated multiple times** (reused across subnets/NICs).
- **Each subnet can have zero or one NSG.** Same for each NIC.
- NSGs assigned to subnets create **protected screened subnets (also called a DMZ)**.

**NSG rule properties** — you create a rule by specifying:

| Property | Values |
|---|---|
| **Name** | Friendly label |
| **Priority** | **100–4096. Rules processed in priority order — the LOWER the number, the HIGHER the priority.** |
| **Port** | Port or range; `*` means any port |
| **Protocol** | Any, TCP, UDP |
| **Source** | Any, IP Addresses, **Service tag**, Application security group |
| **Destination** | Any, IP Addresses, Virtual Network, Application security group |
| **Action** | **Allow or Deny** |
| **Service** | Specifies destination protocol and port range for the rule (e.g. HTTP, RDP, SSH, Custom) |

**Default rules:**
- **Default INBOUND rules deny all inbound traffic EXCEPT from the virtual network and Azure load balancers.**
- **Three default OUTBOUND rules** allow outbound traffic only **to the Internet and the virtual network**.
- Default rules **cannot be deleted** (e.g. `AllowInternetOutbound` at priority **65001**), but you can override them with a **higher-priority (lower-numbered)** custom rule.

**NSG effective rules — the evaluation order** ⚠️
- **NSGs are evaluated independently, and an "allow" rule must exist at BOTH levels** for traffic to pass.
- **Incoming traffic:** the **subnet** NSG is evaluated **first**, then the **NIC** NSG.
- **Outgoing traffic:** the **reverse** — **NIC first**, then subnet.
- To verify what's actually applied to a NIC, use the **Effective security rules** link.

> Exam trick: "Traffic is blocked even though the NIC NSG allows it. Why?" → the **subnet** NSG is denying it; an allow must exist at both levels.

### Application Security Groups (ASGs)
An **ASG** lets you group VM NICs by **application role** (e.g. `asg-web`, `asg-db`) and then write NSG rules that reference the **ASG instead of IP addresses**. When VMs are added or removed, the rules automatically apply — no IP maintenance.

| | **NSG** | **ASG** |
|---|---|---|
| What it is | A **firewall** — a container of allow/deny rules | A **logical grouping of NICs** by application role |
| Contains rules? | **Yes** | **No** — it's used *as a source/destination inside* NSG rules |
| Attached to | Subnet or NIC | Network interfaces (VMs) |
| Benefit | Filters traffic | Removes the need to hard-code/maintain IP addresses |

### Azure Firewall

A **managed, cloud-based network security service** protecting VNet resources — a stateful firewall as a service.

**Features:**
- **Built-in high availability** — no additional load balancers required, nothing to configure
- **Availability Zones** — can be configured during deployment to span multiple AZs
- **Unrestricted cloud scalability** — scales up as much as needed; no budgeting for peak traffic
- **Application FQDN filtering rules** — limit outbound HTTP/S or Azure SQL traffic to a list of FQDNs, **including wildcards**
- **Network traffic filtering rules** — centrally create allow/deny rules by source and destination **IP address, port, and protocol**. **Fully stateful**, so it distinguishes legitimate packets for different connection types. Rules are enforced and logged **across multiple subscriptions and virtual networks**.
- **Threat intelligence** — alert and deny traffic from/to known malicious IPs and domains, sourced from the **Microsoft Threat Intelligence feed**
- **Multiple public IP addresses** — up to **100**

**Firewall rules:**
- **By default, Azure Firewall blocks all traffic.**
- **Three kinds of rules**, processed in this order:

```
1. NAT rules  →  2. Network rules  →  3. Application rules
```
- **Once a rule is found that allows the traffic through, no more rules are checked.**

| Rule type | Use for | Key settings |
|---|---|---|
| **NAT (DNAT)** | **Inbound** traffic — translates & filters inbound traffic to Azure subnets. Translates firewall **public IP:port → private IP:port**. **A NAT rule must be matched by a Network rule to allow traffic to pass.** | Name, Protocol (TCP/UDP), Source Address (`*`=Internet, specific address, or CIDR), Destination Address (firewall's external address), Destination Ports, **Translated Address**, **Translated Port** |
| **Network** | **Any non-HTTP/S traffic**, and subnet-to-subnet communication | Name, Protocol (**TCP, UDP, ICMP** (ping/traceroute), or Any), Source Address, Destination Addresses, Destination Ports |
| **Application** | Define **FQDNs** that can be accessed from a subnet | Name, Source Addresses, Protocol:Port (**HTTP/HTTPS** + port), **Target FQDNs** (wildcards allowed; **FQDN tags** represent groups of FQDNs for well-known Microsoft services — e.g. **Windows Update, App Service Environment, Azure Backup**) |

> Exam trick: "You need to allow VMs to reach `*.contoso.com` over HTTPS" → **Application rule**. "You need to allow SSH between subnets" → **Network rule**. "You need to publish an internal web server on the firewall's public IP" → **NAT rule** (plus a network rule).

### Azure DNS

**Azure DNS** hosts your DNS records for your domains on Azure infrastructure, using the **same credentials, APIs, tools, and billing** as your other Azure services.

**Default and custom domain names:**
- When you create a new tenant, a **default domain** is created with the form **`domainname.onmicrosoft.com`**
- You can **add a custom domain name**
- After adding, it **must be verified** — this demonstrates **ownership** of the domain

**Verifying custom domain names:**
- A custom domain name starts in an **unverified** state and must be verified before use.
- **Only one directory can use a domain name** — the organization that owns it.
- Verification is performed by **adding a DNS record**, which can be an **MX or TXT** record.
- When Azure verifies the presence of the DNS record, it adds the domain name to the subscription.

**DNS zones:**
- A **DNS zone hosts the DNS records for a domain**.
- The **zone name must be unique within the resource group**.
- **The same zone name can be reused in a different resource group.**
- Where **multiple zones share the same name, each instance is assigned different name server addresses**.
- The **root/parent domain is registered at the registrar and pointed to Azure NS**; **child domains are registered in Azure DNS directly**.

**DNS delegation:**
- To delegate your domain to Azure DNS you first need the **name server names for your zone**.
- Once assigned, Azure DNS **automatically creates authoritative NS records** in your zone.
- The **easiest way to find your name servers is through the Azure portal** (Overview blade — **four** Azure DNS name servers).

**Record sets:**
- A **record set** is a **collection of records in a zone that have the same name and are the same type**.
- A record set **cannot contain two identical records**.
- The page info changes depending on the record **Type** selected.

**Common record types:** A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), TXT (text/verification), NS (name server), SOA, SRV, PTR.

**Private DNS zones:**
- Use your **own custom domain names** rather than the Azure-provided names.
- Provides **name resolution for VMs within a virtual network and between virtual networks**.
- Configure **split-horizon** views — a private and a public DNS zone **can share the same name**.
- **A private DNS zone is only accessible from the virtual networks it is linked to** — it cannot be reached from the internet.
- You must add a **virtual network link** for each VNet needing private name resolution.
- **Private DNS zones have NO name server records** (public zones do).

---

## 6. Module 5 — Intersite Connectivity: Peering, VPN, ExpressRoute

### Virtual Network Peering

**Benefits (memorize the five):**

| Benefit | Detail |
|---|---|
| **Private** | Traffic between peered VNets is **private** and stays on the **Microsoft backbone network**. **No public Internet, gateways, or encryption is required.** |
| **Performance** | **Low-latency, high-bandwidth** connection between resources in different VNets |
| **Communication** | Resources in one VNet can communicate with resources in another once peered |
| **Seamless** | Transfer data across **Azure subscriptions, deployment models, and Azure regions** |
| **No disruption** | **No downtime** to resources in either VNet when creating the peering or after |

**Rules and gotchas:**
- **Address spaces of connected networks must NOT overlap.**
- **VNet peering is NON-TRANSITIVE.** ⚠️
- **Gateway transit:** a peered VNet can use a **remote gateway** to gain access to resources in the other VNet. Enable **"Allow Gateway Transit"** in the VNet that owns the gateway so the peer can access resources outside the peering (e.g. on-premises via the hub's VPN gateway).

**Service chaining — how to fake transitivity:**
Because peering is non-transitive, you use **user-defined routes (UDRs) and service chaining**. This allows you to:
- **Implement a multi-level hub-and-spoke architecture**
- **Overcome the limit on the number of VNet peerings per virtual network**

**Hub and spoke:**
- The **hub** VNet hosts shared infrastructure components — a **network virtual appliance** or **VPN gateway**.
- **All spoke VNets peer with the hub.**
- Traffic can flow **through NVAs or VPN gateways in the hub**.

**UDRs and service chaining:**
- Service chaining allows UDRs that **direct traffic from one VNet to the IP address of a VM (virtual appliance) in a peered VNet or a VPN gateway**.
- The **IP address of a VM in a VNet, or a VPN gateway, can be used as the next hop** in a user-defined route.

### VPN Gateway connections — three types

| Connection type | Connects |
|---|---|
| **Site-to-site (S2S)** | **On-premises datacenters** to Azure virtual networks (over IPsec/IKE) |
| **VNet-to-VNet** | **Azure virtual networks** to each other |
| **Point-to-site (User VPN)** | **Individual devices/clients** to Azure virtual networks |

### Implementing a Site-to-Site connection — the steps

1. **Create VNets and subnets.** (For S2S you need to connect to an on-premises location.)
2. **Specify the DNS server (optional)** — only if you need name resolution for resources deployed to the VNet.
3. **Create the Gateway Subnet.**
   - Contains the **IP addresses used by the virtual network gateway**
   - Best to use a CIDR block of **`/28` or `/27`** to allow for future configurations
   - **Gateway VMs** are deployed here and configured with the required VPN gateway settings
   - **Never deploy other resources (e.g. additional VMs) to the gateway subnet**
   - ⚠️ **The gateway subnet MUST be named `GatewaySubnet`**
4. **Create the VPN gateway.**
   - VPN type choice depends on the **make and model of your VPN device** and the kind of connection — **route-based** vs. policy-based
   - Your **SKU choice affects the number of tunnels and the aggregate throughput benchmark**
   - The **VNet containing the GatewaySubnet must be associated with the VPN gateway**
   - **The gateway needs a public IP**
5. **Create the Local Network Gateway.** This represents your **on-premises location**.
   - The name typically **refers to the on-premises location**
   - **IP address / FQDN** of the **on-premises VPN device**
   - **Address Space:** one or more **IP ranges in CIDR notation** defining your **local network's address space**
6. **Create the VPN connection** between the gateways.
   - If your VNets are in the **same subscription, you can use the portal**
   - Verify connections **in the portal or with PowerShell**

**High availability scenarios:** **Active/Standby** and **Active/Active**.

### ExpressRoute

A **private connection** from your on-premises network into Microsoft — it **does not go over the public Internet**.

**Benefits:**
- **Layer 3 connectivity using BGP routes**
- **Redundancy** — dual connections to **Microsoft Enterprise Edge routers (MSEEs)**
- Connectivity to Microsoft cloud services — **Azure, Microsoft 365, Dynamics 365**
- Connectivity to **all regions within a geopolitical region**
- **Global connectivity** with the **ExpressRoute Premium add-on**
- **Across on-premises connectivity** with **ExpressRoute Global Reach**
- Bandwidth options from **50 Mbps to 100 Gbps**

**Flexible billing models:**

| Model | Billing |
|---|---|
| **Unlimited data** | Monthly fee; **free inbound and outbound** traffic |
| **Metered data** | Monthly fee; **all inbound data free**; **outbound charged per GB** |
| **Premium add-on** | Increased routing table limits, increased number of VNets, **global connectivity**, connections to Microsoft 365 and Dynamics 365 |

**Coexisting Site-to-Site VPN and ExpressRoute** for the same VNet — advantages:
- **Site-to-Site VPN as a secure failover path for ExpressRoute**
- Site-to-Site VPN to connect to sites that are **not part of your network but are connected through ExpressRoute**

### Intersite connectivity comparison

| | **VNet Peering** | **VPN Gateway (S2S)** | **ExpressRoute** |
|---|---|---|---|
| Connects | VNet ↔ VNet | On-prem ↔ Azure VNet | On-prem ↔ Microsoft cloud |
| Path | **Microsoft backbone** | **Public internet** (encrypted IPsec tunnel) | **Private circuit** (via connectivity provider) |
| Encryption | **Not required** | **Required** (IPsec) | Not encrypted by default (private) |
| Gateway required? | **No** | **Yes** (VPN gateway + GatewaySubnet) | Yes (ExpressRoute gateway) |
| Bandwidth | Very high, low latency | Limited by gateway SKU | 50 Mbps – 100 Gbps |
| Transitive? | **No** (needs UDR/service chaining) | — | — |
| Reaches M365/Dynamics? | No | No | **Yes** |

---

## 7. Module 6 — Traffic Management: Load Balancer, App Gateway, Routing

### Azure Load Balancer — Layer 4

**Public load balancer:**
- **Maps the public IP address and port number of incoming traffic to the private IP address and port number of the VM.**
- **Mapping is also provided for the response traffic from the VM.**
- Used for internet-facing applications (e.g. the web tier).

**Internal load balancer:**
- Has only a **private** frontend IP; used **inside** the VNet (e.g. balancing traffic from the web tier to the business/database tier). Not reachable from the internet.

**Load Balancer components (the flow):**
```
Frontend IP  →  Load balancing rule  →  Backend pool  →  Health probe
```

| Component | Purpose |
|---|---|
| **Frontend IP configuration** | The IP that accepts incoming connections (public or private) |
| **Backend pool** | The VMs/NICs that receive the traffic |
| **Load balancing rule** | Defines how connections traverse the LB — protocol, frontend port, backend port, session persistence, idle timeout, floating IP |
| **Health probe** | Determines which backend instances are healthy and eligible to receive traffic (protocol + port + interval) |
| **Inbound NAT rule** | Forwards a specific frontend port to a specific backend VM (e.g. RDP to one VM) |

**Load Balancer SKUs:**

| | **Basic** | **Standard** |
|---|---|---|
| Backend pool size | Up to 300 instances | Up to 1000 instances |
| Health probes | TCP, HTTP | TCP, HTTP, HTTPS |
| Availability Zones | Not supported | **Zone-redundant / zonal supported** |
| Public IP | Dynamic possible | **Static** (assigned at creation, released at deletion) |
| Secure by default | Open by default | **Closed to inbound unless an NSG allows it** |
| SLA | None | **99.99%** |

> **Lab 03 note:** "The **Standard SKU provides a static IP address**. Static IP addresses are assigned when the resource is created and released when the resource is deleted."

### Azure Application Gateway — Layer 7

Provides **Layer 7 load balancing, Web Application Firewall (WAF), SSL termination, and end-to-end encryption** to the resources in its backend pool.

**Configuration flow:**
```
Frontend IP  →  Listener  →  Rule  →  Backend instances (backend pool + backend settings)
```

| Component | Purpose |
|---|---|
| **Frontend IP** | Public and/or private IP the gateway listens on |
| **Listener** | Protocol + port (+ hostname for multi-site). **Basic** = single site; **Multi-site** = host-header based |
| **Routing rule** | Binds listener → backend target; has a **priority**; supports **path-based routing** |
| **Backend pool** | Target VMs / NICs / IPs / App Services |
| **HTTP/backend settings** | Port, protocol, **cookie-based affinity**, **connection draining**, probe |
| **Health probe** | Backend health status |

**Key capabilities:**
- **URL/path-based routing** — `/image/*` → image servers, `/video/*` → video servers
- **Multi-site hosting** — several domains on one gateway
- **SSL/TLS termination** at the gateway (offloads crypto from backend servers)
- **Web Application Firewall (WAF)** — protects against OWASP Top 10 (SQL injection, XSS, etc.)
- **Cookie-based session affinity** — keeps a user on the same backend server
- **Connection draining** — gracefully removes backend members during maintenance
- **Autoscaling** and zone redundancy (v2 SKU)

**Requirement:** the Application Gateway requires its own **dedicated subnet of `/27` or larger**.

### Load Balancer vs. Application Gateway vs. Traffic Manager

| | **Load Balancer** | **Application Gateway** | **Traffic Manager** |
|---|---|---|---|
| OSI layer | **Layer 4** (TCP/UDP) | **Layer 7** (HTTP/HTTPS) | **DNS-based** (Layer 7 name resolution) |
| Scope | **Regional** | **Regional** | **Global** |
| Routes based on | IP + port | **URL path, host header, headers** | DNS response / routing method |
| WAF? | No | **Yes** | No |
| SSL termination? | No | **Yes** | No |
| Typical use | Balance TCP traffic across VMs in a VNet | Web app routing, WAF, SSL offload | Route users to the closest/healthiest **region** |

> Exam trick: "Requests to `/images` must go to one set of servers and `/videos` to another" → **Application Gateway**. "Balance traffic across VMs on port 1433" → **Load Balancer**. "Send users to the nearest region" → **Traffic Manager / Front Door**.

### User-Defined Routes (UDRs)

- UDRs **control network traffic by defining the next hop of the traffic flow**.
- The hop can be a **virtual network gateway, virtual network, internet, or virtual appliance**.
- **Each route table can be associated to multiple subnets, but a subnet can only be associated to a SINGLE route table.** ⚠️
- **There are no charges for creating route tables in Microsoft Azure.**

**Steps:** Create a routing table → Create a custom route → **Associate the route table** with a subnet.

**Next hop types:**

| Next hop type | Meaning |
|---|---|
| **Virtual appliance** | Send to an NVA's private IP (you supply the **next hop address**) |
| **Virtual network gateway** | Send to a VPN/ExpressRoute gateway |
| **Virtual network** | Route within the VNet |
| **Internet** | Route to the internet |
| **None** | **Drop the traffic** (black hole) |

**System routes** exist by default (intra-VNet, to internet, to peered VNets). UDRs **override** system routes. Route selection: **UDR > BGP route > system route**; more specific prefix wins.

```powershell
Get-AzEffectiveRouteTable       # view your routing information from PowerShell
```

### Service Endpoints

A **service endpoint provides an identity to your virtual network** for Azure services (e.g. `Microsoft.Storage`, `Microsoft.Sql`).

**Benefits:**
- **Improved security** for your Azure service resources — you can lock a service (like a storage account) down to specific subnets
- **Optimal routing** for Azure service traffic from your virtual network
- **Endpoints always take service traffic directly from your virtual network to the service on the Microsoft Azure backbone network**
- **Simple to set up with less management overhead**

### Private Link / Private Endpoint

**A Private Link brings services to your private virtual network by mapping it to a private endpoint, eliminating data exposure to the public internet.**

**Features:**
- **Private connectivity to services on Azure**
- **Integration with on-premises and peered networks**
- **Protection against data exfiltration** for Azure resources
- **Services delivered directly to your customers' virtual networks**

### Service Endpoint vs. Private Endpoint

| | **Service Endpoint** | **Private Endpoint (Private Link)** |
|---|---|---|
| What it does | Extends your **VNet identity** to the Azure service | Gives the service **a private IP inside your VNet** |
| Public IP still used? | **Yes** — traffic still goes to the service's public endpoint (over the backbone) | **No** — the service is reached at a **private IP** |
| Reachable from on-prem / peered VNets? | **No** | **Yes** |
| Data exfiltration protection | Limited | **Yes** |
| Cost | **Free** | Charged |
| Granularity | The **whole service** on that subnet | **A specific resource instance** |

---

## 8. Module 7 — Azure Storage

### Storage accounts

An **Azure storage account contains all of your Azure Storage data objects**: **blobs, file shares, queues, tables, and disks**. It provides a **unique namespace** for your data, accessible from anywhere in the world over **HTTP or HTTPS**.

**Azure Storage is:**
- **Durable and highly available** — redundancy and replication across datacenters/geographic regions
- **Secure** — all data written is **encrypted**, with fine-grained access control
- **Scalable** — massively scalable
- **Managed** — Microsoft handles hardware maintenance, updates, critical issues
- **Accessible** — over HTTP or HTTPS from anywhere

**Three categories of Azure storage:**

| Category | Contains |
|---|---|
| **Storage for VMs** | **Disks and files** |
| **Unstructured data** | **Blobs** (highly scalable, REST-based cloud object store) and **Data Lake Store** (HDFS as a service) |
| **Structured data** | **Tables** (key/value, autoscaling NoSQL store), **Cosmos DB**, **Azure SQL DB** |

**General purpose storage accounts have two performance tiers: Standard and Premium.**
> Use **Standard** for most applications; use **Premium** for enterprise or high-performance applications.

**Azure Storage data services:**

| Service | Description |
|---|---|
| **Azure Containers (Blobs)** | A massively scalable **object store** for text and binary data |
| **Azure Tables** | Ideal for storing **structured, non-relational** data |
| **Azure Queues** | A **messaging store** for reliable messaging between application components |
| **Azure Files** | **Managed file shares** for cloud or on-premises deployments (SMB) |

**All storage accounts are encrypted using Storage Service Encryption (SSE) for data at rest.**

### Replication / redundancy options ⚠️ *heavily tested*

| Option | Replicas | Regions | Zones | Protects against | Write behavior |
|---|---|---|---|---|---|
| **LRS** — Locally Redundant | **3** | 1 | 1 | **Disk, node, rack** failures | Write acknowledged when **all replicas committed**; superior to dual-parity RAID |
| **ZRS** — Zone Redundant | **3** | 1 | **3** | Disk, node, rack, **+ zone** failures | **Synchronous** writes to all three zones |
| **GRS** — Geo Redundant | **6** (3 per region) | **2** | 1 each | **+ major regional disasters** | **Asynchronous** copy to secondary |
| **RA-GRS** — Read-Access GRS | 6 | 2 | 1 each | Same as GRS **+ read access to secondary** | Separate **secondary endpoint**; **RPO delay to secondary can be queried** |
| **GZRS** — Geo-Zone Redundant | **6** | **2** | **3 + 1** | Disk, node, rack, **zone, AND region** | **Synchronous to all 3 zones + asynchronous** copy to secondary |
| **RA-GZRS** | 6 | 2 | 3+1 | Same as GZRS + read access | Separate secondary endpoint; RPO queryable |

**How to answer redundancy questions:**
- Cheapest / only local protection → **LRS**
- Protect from a **datacenter/zone** failure within a region → **ZRS**
- Protect from a **regional** disaster → **GRS**
- Need to **read** data during a regional outage → **RA-GRS** (add "RA-" whenever the question says *read* or *read access during outage*)
- Highest protection, both zone and region → **GZRS / RA-GZRS**

### Accessing storage — endpoint URLs

Every object has a **unique URL**; the **storage account name forms the subdomain**. For `mystorageaccount`:

| Service | Endpoint |
|---|---|
| Container (blob) | `http://mystorageaccount.blob.core.windows.net` |
| Table | `http://mystorageaccount.table.core.windows.net` |
| Queue | `http://mystorageaccount.queue.core.windows.net` |
| File | `http://mystorageaccount.file.core.windows.net` |

A **custom domain name** can also be configured.

### Securing storage endpoints
- **Firewalls and Virtual Networks** restrict access to the storage account **from specific subnets on virtual networks or public IPs**.
- **Subnets and virtual networks must exist in the same Azure region or region pair as the storage account.**

### Blob storage

**Azure Blob storage** is a service for storing **large amounts of unstructured object data** (text or binary). Also called **object storage**.

**Common uses:**
- Serving images or documents **directly to a browser**
- Storing files for **distributed access**, such as installation
- **Streaming video and audio**
- Storing data for **backup and restore, disaster recovery, and archiving**
- Storing data for **analysis** by an on-premises or Azure-hosted service

**Three types of blob resources:** the **storage account** → **containers** → **blobs**.

**Containers:**
- A container provides a **grouping of a set of blobs**
- **All blobs must be in a container**
- An account can contain an **unlimited number of containers**
- A container can store an **unlimited number of blobs**

**Blob access tiers:**

| Tier | Access pattern | Minimum storage duration | Retrieval |
|---|---|---|---|
| **Hot** | Frequent access | — | Immediate |
| **Cool** | Infrequent access | **At least 30 days** | Immediate |
| **Archive** | Rare access | **At least 180 days** | **Several hours retrieval latency** |

**You can switch access tiers at any time.**

**Blob types** ⚠️

| Type | Use | Detail |
|---|---|---|
| **Block blob** (**default**) | Text and binary data — files, images, videos | The general-purpose blob |
| **Append blob** | **Logging scenarios** | Optimized for **append** operations |
| **Page blob** | **Azure VM OS and data disks** | Up to **8 TB**; efficient for **frequent read/write** operations |

**⚠️ Once the blob has been created, its TYPE cannot be changed.** (The *tier* can.)

**Object replication:** asynchronously copies **block blobs** in a container according to configured rules.
- Benefits: **minimizing latency**, **increasing efficiency for compute workloads**, **optimizing data distribution**
- Considerations: **blob versioning must be enabled on source and destination accounts**; **doesn't support blob snapshots**; **source and destination accounts must be in the hot or cool tier**
- A **replication policy** must be created, containing **one or more rules**

**Blob upload tools:**

| Tool | Description |
|---|---|
| **AzCopy** | **Command-line tool** for Windows and Linux |
| **Azure Storage Data Movement library** | **.NET library** for moving data |
| **Azure Data Factory** | Supports **managed identities** for Azure resource authentication |
| **Blobfuse** | **Virtual file system driver** for the Linux file system |
| **Azure Data Box Disk** | Copy data to disks and **ship them to Microsoft**; **1–5 disks, max 35 TB** |
| **Azure Import/Export service** | **Export** large amounts of data to hard drives **you provide**; Microsoft ships them back with your data |
| **Azure Storage Explorer** | Standalone GUI app (Windows/macOS/Linux) |

**Storage pricing factors:**
- **Performance tiers** — as the tier gets **cooler**, the **per-GB storage cost decreases**
- **Data access costs** — **increase** as the tier gets cooler (cool and archive charge a per-GB data access charge for reads)
- **Transaction costs** — per-transaction charge for all tiers, **increases as the tier gets cooler**
- **Geo-replication data transfer costs** — applies to geo-replicated accounts
- **Outbound data transfer costs** — bandwidth billed per GB
- **Changing the storage tier** — incurs a charge

> **The tradeoff to remember:** cooler tier = **cheaper to store**, **more expensive to access**.

### Storage security

| Mechanism | What it does |
|---|---|
| **Encryption (SSE)** | All data written is **automatically encrypted** |
| **Authentication** | Provided by **Microsoft Entra ID and RBAC** |
| **Data in transit** | Secured by **Client-Side Encryption, HTTPS, or SMB 3.0** |
| **Disk encryption** | OS and data disks used by Azure VMs encrypted with **Azure Disk Encryption** |
| **Shared Access Signatures (SAS)** | **Delegated access** to data objects |
| **Shared Key** | Used for **authorization** (the account access keys) |
| **Anonymous access** | You can optionally make blob resources **public at the container or blob level** |

**Storage Service Encryption (SSE):**
- Protects your data for **security and compliance**
- **Automatically encrypts and decrypts** your data
- **256-bit AES** encryption
- **Enabled for all new and existing storage accounts and CANNOT be disabled** ⚠️
- **Transparent to users**

**Shared Access Signatures (SAS):**
- A SAS is a **URI that grants restricted access rights to Azure Storage resources**
- It's a **signed URI** that points to one or more storage resources
- The URI = **your storage resource URI + the SAS token**
- Parameters include: **resource URI, storage services version, services, resource types, start time, expiry time, resource, permissions, IP range, protocol, and signature**

Example:
```
https://myaccount.blob.core.windows.net/?restype=service&comp=properties&sv=2015-04-05
&ss=bf&srt=s&st=2015-04-29T22:18:26Z&se=2015-04-30T02:23:26Z&sr=b&sp=rw
&sip=168.1.5.60-168.1.5.70&spr=https&sig=F%6GRVAZ5Cdj2Pw4txxxxx
```

**SAS / storage security best practices** (short-answer gold):
1. **Always use HTTPS** to create or distribute a SAS
2. **Reference stored access policies where possible** (lets you revoke without regenerating keys)
3. Use **near-term expiration times** on an unplanned SAS
4. Have clients **automatically renew** the SAS if necessary
5. **Be careful with SAS start time** (clock skew — set it slightly in the past)
6. **Be specific** with the resource to be accessed
7. Understand that **your account will be billed for any usage**, including via SAS
8. **Validate data written using SAS**
9. **Don't assume SAS is always the correct choice**
10. Use **Storage Analytics** to monitor your application

### Azure Files

**File storage offers shared storage for applications using the industry standard SMB protocol.**

**Common uses:**
- **Replace and supplement file servers or NAS devices**
- **Access from anywhere** — Windows, macOS, and Linux can directly mount Azure File shares
- **Lift and shift** applications to the cloud that expect a file share
- **Azure File Sync** can replicate Azure File shares to Windows Servers, on-premises or in the cloud
- Store **shared application settings**
- Store **diagnostic data** — logs, metrics, crash dumps
- Store **tools and utilities** needed for developing/administering Azure VMs

### Azure Files vs. Azure Blobs

| | **Azure Files** | **Azure Blobs** |
|---|---|---|
| Interface | **SMB interface**, client libraries, and a **REST interface** | Client libraries and a **REST interface** |
| Structure | **Hierarchical** (directories) | **Flat namespace** |
| When to use | Lift and shift an application to the cloud · Store **shared data across multiple VMs** · Store dev/debug tools accessed from many VMs | Support **streaming and random-access** scenarios · Access **application data from anywhere** · **Massive scale** unstructured data in block blobs |

> Exam trick: "Multiple VMs need to access the **same** files / you need a drive letter / SMB" → **Azure Files**. "Serve images to a browser / stream video / massive unstructured data" → **Blob**.

### File share snapshots
- Capture a **point-in-time, read-only copy** of your data
- **Share snapshot capability is provided at the file SHARE level. Retrieval is provided at the individual FILE level.** ⚠️
- **You cannot delete a share that has share snapshots unless you delete all the share snapshots first.**

### Azure File Sync

Use Azure File Sync to **centralize your organization's file shares in Azure Files while keeping the flexibility, performance, and compatibility of an on-premises file server.**

**Uses/advantages:** **Lift and shift · Branch Offices · Backup and Disaster Recovery · File Archiving** (cloud tiering).

**Components (memorize all six):**

| Component | Definition |
|---|---|
| **Storage Sync Service** | The **top-level resource** |
| **Registered server** | Represents a **trust relationship** between your server (or cluster) and the Storage Sync Service |
| **Azure File Sync agent** | A **downloadable package** enabling Windows Server to sync with an Azure file share |
| **Server endpoint** | A **specific location on a registered server**, such as a folder |
| **Cloud endpoint** | **An Azure file share** |
| **Sync group** | **Defines which files are kept in sync** (contains one cloud endpoint + one or more server endpoints) |

### Managing storage — tools

| Tool | Key facts |
|---|---|
| **Azure Storage Explorer** | Standalone app for **Windows, macOS, and Linux**. Access **multiple accounts and subscriptions**; create/delete/view/edit storage resources; view and edit **Blob, Queue, Table, File, Cosmos DB and Data Lake Storage**; **obtain SAS keys** |
| **AzCopy** | **Command-line tool** for Windows and Linux |
| **Azure Data Box Disk** | Microsoft ships you **1 to 5 disks**, max capacity **35 TB**; you copy data and ship them back |
| **Azure Import/Export service** | Export large amounts of data to **hard drives you provide** |

---

## 9. Module 8 — Virtual Machines

### IaaS — shared responsibility
With **IaaS**, Microsoft manages the **physical hosts, network, and datacenter**; **you** manage the **OS, patching, applications, runtime, and data**. (Compare: **PaaS** — Microsoft also manages the OS/runtime; **SaaS** — Microsoft manages everything.)

**IaaS business scenarios:** Test and development · Website hosting · Storage, backup, and recovery · **High-performance computing (HPC)** · Big data analysis · **Extended datacenter**.

### VM planning — the checklist

| Decision | Notes |
|---|---|
| **Start with a Virtual Network (VNet)** | VNets provide connectivity between VMs and other Azure services |
| **Name the VM** | The VM name is used as the **computer name**. Use meaningful, consistent names. Example: **`deveus-webvm01`** = first **dev**elopment **web** server in the **US** South Central location |
| **Decide the location (region)** | Available options and **price differences between locations** |
| **Determine the size** | Based on the **type of workload** the VM needs to run. **When you stop and deallocate a VM, you can select any size available in your region** |
| **Understand the pricing model** | Compute (per-hour, stops when deallocated) + storage (charged even when stopped) |
| **Storage for the VM** | Disk types |
| **Select an operating system** | Windows / Linux image |

**VM size families:** General purpose (B, D), Compute optimized (F), Memory optimized (E, M), Storage optimized (L), GPU (N), High performance compute (H).

### VM storage — every VM has at least two disks ⚠️

| Disk | Details |
|---|---|
| **Operating system disk** | Every VM has **one** attached OS disk with a **pre-installed OS** selected at creation. **Registered as a SATA drive and labeled the `C:` drive by default.** |
| **Temporary disk** | Every VM has one. **NOT a managed disk.** Provides **short-term storage** for applications and processes; intended **only for data such as page or swap files**. **Data here is LOST on deallocation/host maintenance** — never store anything you need on it. (Usually `D:` on Windows.) |
| **Data disk** | **Optional** managed disk attached to store **application data** or other data you need to keep |

**Managed disk types:** Standard HDD → Standard SSD → Premium SSD → Ultra Disk (increasing performance and cost).

### Creating a VM in the portal — the tabs

| Tab | Contains |
|---|---|
| **Basics** | Project details, **administrator account**, **inbound port rules**, name, region, availability options, image, size |
| **Disks** | **OS disk type**, data disks |
| **Networking** | Virtual networks, subnet, public IP, NSG, **load balancing** |
| **Management** | **Monitoring, auto-shutdown, backup** |
| **Advanced** | Additional configuration, **agents, scripts, or applications via VM extensions or cloud-init** |

### VM connections

| VM type | Connection method |
|---|---|
| **Windows** | **Remote Desktop Protocol (RDP)** — port **3389**. Also **Windows Remote Management (WinRM)** — establishes a **command-line session** to a VM running any supported version of Windows |
| **Linux** | **Secure Shell (SSH)** client such as **PuTTY** — port **22**. Authenticate with an **SSH public key or a password** |
| **Any** | **Azure Bastion** — provides **secure RDP and SSH connectivity to all VMs in the virtual network in which it is provisioned**, straight from the browser, with **no public IP on the VM** |

> Exam trick: "Connect to VMs securely without exposing public IPs / without opening 3389" → **Azure Bastion**.

### VM availability

**Three scenarios that impact a VM:**

| Scenario | Description |
|---|---|
| **Unplanned hardware maintenance** | Azure **predicts** the hardware or a platform component is **about to fail** |
| **Unexpected downtime** | The hardware or physical infrastructure **fails unexpectedly** |
| **Planned maintenance** | **Periodic updates by Microsoft** to the underlying platform to improve reliability, performance, and security |

**Availability Sets:**
- An availability set **prevents a single point of failure** for VMs
- VMs in an availability set should **perform an identical set of functionalities and have the same software installed**
- For redundancy, **configure multiple VMs in an availability set**
- **Configure each application tier into SEPARATE availability sets** (web tier in one, DB tier in another)
- **Combine a load balancer with availability sets**
- **Use managed disks** with the VMs

**Update and Fault Domains:**

| | Definition |
|---|---|
| **Update Domain (UD)** | During **planned maintenance**, **only one update domain is rebooted at a time**. By default there are **five (non-user-configurable) update domains**, but you **can configure up to 20**. |
| **Fault Domain (FD)** | Defines a group of VMs that **share a common set of hardware and switches** — a **single point of failure**. Example: a **server rack** serviced by a set of power or networking switches. |

> Mnemonic: **U**pdate = **U**pgrade/reboot (planned, software). **F**ault = **F**ailure (unplanned, hardware/power/network).

**Availability Zones:**
- **Unique physical locations within an Azure region**
- Each zone is made up of **one or more datacenters with independent power, cooling, and networking**
- **Minimum of three separate zones in all enabled regions**
- **Physical separation protects applications and data from datacenter failures**
- **Zone-redundant services** replicate applications and data across zones
- **Industry best 99.99% VM uptime SLA**

**SLA table (memorize):**

| Configuration | SLA |
|---|---|
| **2+ VMs across 2+ Availability Zones** in the same region | **99.99%** |
| **2+ VMs in an Availability Set** | **99.95%** |
| **Single VM** using **premium storage** | **99.9%** |

### Scaling

| | **Vertical scaling** | **Horizontal scaling** |
|---|---|---|
| Also called | **Scale up / scale down** | **Scale out / scale in** |
| What changes | **Increasing or decreasing VM sizes** in response to a workload | **The number of VMs** is altered depending on workload |
| Limitations | **Generally has more limitations** (max VM size; requires restart) | **More flexible in a cloud situation** |

**Reprovisioning** means **removing an existing virtual machine and replacing it with a new one**.

**Virtual Machine Scale Sets (VMSS):**
- A group of **identical, load-balanced VMs** that can **automatically increase or decrease the number of VM instances** running your application — **dynamically scale to meet changing demand**
- **Autoscaling can be scheduled** to increase or decrease capacity at fixed times
- **Orchestration modes:** **Uniform** (identical VMs from a single config — used in Lab 05) and **Flexible** (mix of VM types/configs)
- Can be deployed across **availability zones**

**Autoscale rule anatomy (from Lab 05):** metric source → metric namespace → **metric name** (e.g. *Percentage CPU*) → **operator** (Greater than / Less than) → **threshold** → **duration** → **time grain statistic** (Average) → **operation** (Increase count by / Decrease count by / Increase percent by) → **cool down** → **instance count**. Plus **instance limits: minimum, maximum, default**.

### VM Extensions
- **Small applications that provide post-deployment VM configuration and automation tasks**
- Managed with **Azure CLI, PowerShell, ARM templates, and the Azure portal**
- Can be **bundled with a new VM deployment or run against any existing system**
- **Different for Windows and Linux machines**

**Custom Script Extension** — downloads and runs a script on the VM (e.g. install IIS after deployment). **Cloud-init** is the Linux equivalent used at provisioning time.

---

## 10. Module 9 — App Service & Containers

### App Service Plans

An **App Service plan defines a set of compute resources for a web app to run**. **One or more apps can run on the same computing resources in the plan.**

**Each App Service plan defines:**
- **Region** (West US, East US, etc.)
- **Number of VM instances**
- **Size of VM instances** (Small, Medium, Large)

**Pricing tiers:** Free · Shared · Basic · Standard · Premium · Isolated (increasing features, scale, and isolation).

### Scaling a web app — two workflows

| | **Scale UP** | **Scale OUT** |
|---|---|---|
| What it does | **Get more CPU, memory, disk space, and extra features by changing the App Service Plan** (pricing tier) | **Increase the number of VM instances** that run your app |
| Analogy | Bigger machine | More machines |
| Reversible? | Yes — **scale up and down at any time**; as simple as **changing the pricing tier**. Start at a lower tier and scale up later; scale down to save money | Yes — **add resources for load, remove idle resources to save money** |
| Automatic? | Manual | **Autoscaling**: scales based on a **metric** (**CPU percentage, memory percentage, HTTP requests**) or **according to a schedule** (weekdays, weekends, times, holidays) |

### Azure App Service

**Azure App Service brings together everything you need to create websites, mobile backends, and web APIs for any platform or device.**

**Features:**
- **Multiple languages and frameworks** (.NET, Java, Node.js, PHP, Python, Ruby)
- **DevOps optimization**
- **Global scale with high availability**
- **Connections to SaaS platforms and on-premises data**
- **Security and compliance** — App Service is **ISO, SOC, and PCI compliant**
- **Application templates**
- **Visual Studio integration**
- **API and mobile apps support**
- **Serverless code**

**Creating an App Service:**
- **Name must be unique** (globally)
- Access using **`azurewebsites.net`** — can map to a **custom domain**
- **Publish: Code (runtime stack)** or **Docker Container**
- **Linux or Windows**
- **Region** closest to your users
- **App Service Plan**

### Continuous Deployment
The Azure portal provides out-of-the-box CI/CD with **Azure DevOps, GitHub, Bitbucket, FTP, or a local Git repository** on your development machine. **Whenever code updates are pushed to source control, the website or web app automatically picks up the updates.**

> **Lab 06 tie-in:** you used **Deployment Center → Settings → Source: External Git** with repo `https://github.com/Azure-Samples/php-docs-hello-world`, branch `master`.

### Deployment Slots ⚠️ *high-yield*

| Tier | Slots available |
|---|---|
| Free, Shared, Basic | **0** |
| Standard | **Up to 5** |
| Premium | **Up to 20** |
| Isolated | **Up to 20** |

**Why use slots:**
- **Deploy to a different deployment slot** (depends on service plan)
- **Validate changes before sending to production**
- **Deployment slots are live apps with their own hostnames**
- **Avoids a cold start — eliminates downtime**
- **Fallback to a last known good site** (swap back)
- **Auto Swap** when pre-swap validation is not needed

**Creating slots:**
- New deployment slots can be **empty or cloned**
- **Slot settings fall into three categories:**
  1. **Slot-specific app settings and connection strings**
  2. **Continuous deployment settings**, if enabled
  3. **App Service authentication settings**, if enabled
- **Not all settings are "sticky"** (i.e., these follow the swap rather than staying with the slot): **endpoints, custom domain names, SSL certificates, scaling**

### Securing an App Service
Azure App Service provides **built-in authentication and authorization support**, so you can sign in users and access data by **writing minimal or no code** in your web app, API, mobile back end, and **Azure Functions**. Many web frameworks bundle their own security features and you can use those instead.

### Custom domain names
When you create a web app, Azure assigns it a **subdomain of `azurewebsites.net`**. For production you may want a custom domain.

**Steps:**
1. **Register your domain name**
2. **Create DNS records that map the domain to your Azure web app**
3. **Create a CNAME or A record with the mapping**

### App Service backup
- Create backups **manually or on a schedule**
- Backs up the **configuration, file content, and database connected to the app**
- **Requires a Standard or Premium plan** ⚠️
- Backups can be **up to 10 GB** of app and database content
- Configure **partial backups** and **exclude items**
- **Restore on-demand to a previous state, or create a new app**

### Application Insights
**Application Insights, a feature of Azure Monitor, monitors your live applications.**

Features: **Request rates, deny rates, response time and failure rates** · **Page views and load performance** · **User and session counts** · **Performance counters** · **Diagnostics and exceptions**.

### Container services

**Containers offer a standardized and repeatable way to package, deploy and manage cloud applications.**

**Azure Container Instances (ACI)** lets you **run a container in Azure without managing virtual machines and without a higher-level service.**

**Advantages of containers over physical and virtual machines:**
- **Increased flexibility and speed** when developing and sharing application code
- **Simplified application testing**
- **Streamlined and accelerated application deployment**
- **Higher workload density**, resulting in **improved resource utilization**

### Containers vs. Virtual Machines ⚠️ *classic short-answer*

| Feature | **Containers** | **Virtual Machines** |
|---|---|---|
| **Isolation** | **Lightweight** isolation from host and other containers; **NOT as strong a security boundary as a VM** | **Complete isolation** from the host OS and other VMs — useful when a strong security boundary is critical (hosting apps from **competing companies** on the same server/cluster) |
| **Operating system** | Runs the **user mode portion** of an OS; can be tailored to contain **just the needed services**, using **fewer system resources** | Runs a **complete OS including the kernel**, requiring **more resources** (CPU, memory, storage) |
| **Deployment** | Deploy individual containers with **Docker via command line**; deploy multiple with an **orchestrator such as Azure Kubernetes Service (AKS)** | Deploy individual VMs with **Windows Admin Center or Hyper-V Manager**; multiple with **PowerShell or System Center VMM** |
| **Persistent storage** | **Azure Disks** for local storage on a single node; **Azure Files (SMB shares)** for storage shared by multiple nodes/servers | **VHD** for local storage for a single VM; **SMB file share** for storage shared by multiple servers |
| **Fault tolerance** | If a cluster node fails, containers on it are **rapidly recreated by the orchestrator on another node** | VMs can **fail over to another server in a cluster**, with the VM's OS **restarting** on the new server |

### Container groups
A **container group is a collection of containers that get scheduled on the same host machine.**

A container group:
- Is **scheduled on a single host machine**
- Is **assigned a DNS name label**
- **Exposes a single public IP address, with one exposed port**
- Example: **consists of two containers** — one listening on **port 80**, the other on **port 1433**
- **Includes two Azure file shares as volume mounts**, each container mounting one locally

### Docker

**Docker is a platform that enables developers to host applications within a container.** A **container** is a **standalone package containing everything needed to execute a piece of software**: the **application executable code, the runtime environment (such as .NET Core), system tools, and settings**.

**Docker terminology:**

| Term | Definition |
|---|---|
| **Container** | An **instance of a Docker image**, an execution environment, and a standard set of instructions |
| **Container image** | A **package with all the dependencies and information required to create a container** |
| **Build** | The action of **building a container image** based on the info/context in the Dockerfile |
| **Pull** | **Downloading** a container image **from** a container registry |
| **Push** | **Uploading** a container image **to** a container registry |
| **Dockerfile** | A **text file with instructions on how to build a Docker image** — like a batch script. **The first line identifies the base image**; the rest includes the build actions |

**Azure container options ladder:** **ACI** (single containers, no orchestration) → **Azure Container Apps** (managed serverless containers; abstracts the Kubernetes cluster) → **AKS** (full Kubernetes cluster you manage) → **Azure Container Registry (ACR)** (private image registry).

> **Lab 06 note:** *"Azure Container Apps take the concept of a managed Kubernetes cluster a step further and manage the cluster environment as well... Unlike an Azure Kubernetes cluster, where you must still manage the cluster, an Azure Container Apps instance removes some of the complexity."* By default a container app **accepts traffic on port 80** and Azure provides a **DNS name** for the application.

---

## 11. Module 10 — Data Protection: Backup & Site Recovery

### Azure Backup — key benefits
- **Offload on-premises backup**
- **Back up Azure IaaS VMs**
- **Unlimited data transfer** (no charge for inbound/outbound backup transfer)
- **Keep data secure**
- **Get app-consistent backups**
- **Retain short and long-term data**
- **Automatic storage management**
- **Multiple storage options:** **Locally redundant storage (LRS)** and **Geo-redundant storage (GRS)**

### Azure Backup Center
**A single unified management experience to govern, monitor, operate, and analyze backups at scale.**
- **Single pane of glass** — efficiently manage backups spanning **multiple workload types, vaults, subscriptions, regions, and tenants**
- **Datasource-centric management** — a resource owner or backup admin can administer backup items **across different vaults**; filter views by **subscription, datasource resource group, and datasource tags**
- **Connected experiences** — native integrations to existing Azure services; uses **Azure Workbooks and Azure Monitor Logs** for detailed backup reports

### Recovery Services Vault
**The Recovery Services vault is a storage entity in Azure that stores data.**

**Backup options:**
- Back up **Azure file shares**
- Back up **on-premises files and folders**
- Back up **Azure VMs**
- Back up **on-premises VMs**

> Lab 07 note: **Azure has two types of vaults — Recovery Services vaults and Backup vaults. The main difference is the datasources that can be backed up.**
> Also: the **storage replication type can only be configured if there are NO existing backup items.**

### Implementing on-premises file and folder backup — the 4 steps

1. **Create the Recovery Services vault** in your Azure subscription
2. **Download the agent and credential file** — the vault provides a link to download the **Azure Backup Agent (MARS)**; a **credentials file is required during installation**. You must have the **latest version** — versions **below 2.0.9083.0 must be upgraded by uninstalling and reinstalling** the agent
3. **Install and register the agent** — the installer wizard configures **installation location, proxy server, and passphrase**; the downloaded **credential file registers the agent**
4. **Configure the backup** — create a backup policy including **when to back up, what to back up, how long to retain items**, and settings like **network throttling**

### MARS agent (Microsoft Azure Recovery Services agent)
- Installed on the **Windows client or server**
- **Backs up files and folders on physical or virtual Windows OS** (VMs can be on-premises or in Azure)
- **No separate backup server required**
- **NOT application aware** — **file, folder, and volume-level restore only**
- **Backup 3x per day**
- **No support for Linux**
- Backup storage: **Recovery Services vault**

### VM data protection options

| Option | Use case |
|---|---|
| **Azure Backup** | Backing up Azure VMs running **production workloads**. Supports **application-consistent backups for both Windows and Linux** VMs |
| **Azure Site Recovery** | Protects VMs from **a major disaster scenario when a whole region experiences an outage**. Recover with a **single click**; replicate to **an Azure region of your choice** |
| **Managed disk snapshots** | For **development and test** environments — **quick and simple**. Back up managed disks at any point in time. Snapshots **exist independent of the source disk** and can be used to **create new managed disks** |
| **Images** | Create a **managed custom image** from a custom VHD in a storage account or **directly from a generalized (sysprepped) VM**. Captures a single image that **enables creating hundreds of VMs** |

### Virtual machine snapshots — the two phases of a backup job
1. **A virtual machine snapshot is taken**
2. **The snapshot is transferred to the Azure Recovery Services vault**

**Features:**
- **Reduces backup and restore times by retaining snapshots locally, for two days by default**
- **This default snapshot retention value is configurable to any value between 1 to 5 days**
- **Supports disk sizes up to 32 TB**
- **Ability to use snapshots taken as part of a backup job for recovery WITHOUT waiting for data transfer to the vault to finish**

### Implementing VM backups — the steps
1. **Create a Recovery Services vault in the region where you want to store the data.**
   - **If Azure is your PRIMARY backup storage endpoint → use the default geo-redundant storage (GRS)**
   - **If Azure is a NON-PRIMARY backup storage endpoint → choose locally redundant storage (LRS)**, which reduces cost
2. **Use the portal to define the backup** and protect data by taking snapshots at defined intervals. These snapshots are known as **recovery points**, stored in the Recovery Services vault
3. **Back up the virtual machine.** The **Azure VM Agent must be installed** on the VM for the Backup extension to work. **If your VM was created from the Azure gallery, the VM Agent is already present.**

**Implementing VM restore:** when you start the restore, the Backup service **creates a job for tracking the restore operation** and **creates and temporarily displays notifications** so you can monitor progress.

### Azure Backup Server (MABS) / Data Protection Manager (DPM)
- Another method for backing up VMs, used for **specialized workloads, VMs, or files/folders/volumes**
- Provides **app-aware backups optimized for common apps** — **SQL Server, Exchange, and SharePoint**
- **Each machine runs the DPM/MABS protection agent; the MARS agent runs on the MABS/DPM server only**

### Backup component comparison ⚠️

| | **Azure Backup (MARS) agent** | **Azure Backup Server (MABS) / DPM** |
|---|---|---|
| **Benefits** | Back up **files and folders** on physical or virtual **Windows** OS; **no separate backup server required** | **App-aware snapshots**; **full flexibility for when to run backups**; **recovery granularity**; **Linux support on Hyper-V and VMware VMs**; back up and restore **VMware VMs**; **doesn't require a System Center license** |
| **Limits** | **Backup 3x per day**; **not application aware**; **file, folder, and volume-level restore only**; **no support for Linux** | **Cannot back up Oracle workloads**; **always requires a live Azure subscription**; **no support for tape backup** |
| **Protects** | **Files, Folders** | **Files, Folders, Volumes, VMs, Applications, Workloads** |
| **Backup storage** | **Recovery Services vault** | **Recovery Services vault** and **locally attached disk** |

### Soft Delete
**Even after a backup is deleted, it is preserved in soft-delete state for 14 additional days.**

> **Lab 07 practical consequence:** because soft delete is enabled, **simply deleting your resource groups will NOT delete the Recovery Services Vault.** You must delete the backups and the RSV first (the portal offers **"Delete using PowerShell script"** — generate it and run it in Cloud Shell).

### Azure Site Recovery (ASR)
**Site Recovery replicates workloads running on physical and virtual machines from a primary site to a secondary location.** When an outage occurs at your primary site you **fail over** to the secondary location and access apps from there. After the primary location is running again, you can **fail back**.

**Replication scenarios:**
- Replicate **Azure VMs from one Azure region to another**
- Replicate **on-premises VMware VMs, Hyper-V VMs, physical servers (Windows and Linux), Azure Stack VMs → to Azure**
- Replicate **AWS Windows instances → to Azure**
- Replicate on-premises **VMware VMs, Hyper-V VMs managed by System Center VMM, and physical servers → to a secondary site**

### Backup vs. Site Recovery — the distinction the exam wants

| | **Azure Backup** | **Azure Site Recovery** |
|---|---|---|
| Protects against | **Data loss** — accidental deletion, corruption, ransomware | **Site/region outage** — disaster recovery |
| Granularity | File / folder / volume / VM **recovery points** | **Whole-VM replication** with failover |
| RPO/RTO | Higher (scheduled, e.g. daily) | **Continuous replication**, low RPO, fast failover |
| Operation | **Restore** | **Fail over** / **fail back** |
| Target | Recovery Services vault | Vault in a **different region** |

---

## 12. Module 11 — Monitoring: Azure Monitor, Alerts, Log Analytics, Network Watcher

### Azure Monitor
**Monitoring is the act of collecting and analyzing data.** Azure includes multiple services that each perform a specific role in the monitoring space.

**Key capabilities (three):**

| Capability | Detail |
|---|---|
| **Monitor and visualize metrics** | **Metrics are numerical values available from Azure resources** helping you understand the **health, operation, and performance** of your system |
| **Query and analyze logs** | **Logs are activity logs, diagnostic logs, and telemetry from monitoring solutions**; analytics queries help with **troubleshooting and visualizations** |
| **Set up alerts and actions** | **Alerts notify you of critical conditions and potentially take automated corrective actions** based on triggers from **metrics or logs** |

### Metrics vs. Logs ⚠️ *all data collected by Azure Monitor fits into one of these two fundamental types*

| | **Metrics** | **Logs** |
|---|---|---|
| Definition | **Numerical values that describe some aspect of a system at a particular point in time** | **Different kinds of data organized into records with different sets of properties for each type** |
| Character | **Lightweight**, capable of supporting **near real-time** scenarios | **Events and traces** stored as logs, in addition to performance data, so it can all be **combined for analysis** |
| Queried with | Metrics Explorer / charts | **Kusto Query Language (KQL)** in Log Analytics |

### Data types Azure Monitor collects (five tiers)

| Tier | What it covers |
|---|---|
| **Application monitoring data** | Performance and functionality of **the code you have written**, regardless of platform |
| **Guest OS monitoring data** | The **operating system** your application runs on (in Azure, another cloud, or on-premises) |
| **Azure resource monitoring data** | The operation of **an Azure resource** |
| **Azure subscription monitoring data** | The **operation and management of a subscription**, plus the **health and operation of Azure itself** |
| **Azure tenant monitoring data** | **Tenant-level Azure services, such as Entra ID** |

### Activity Log ⚠️

**The Azure Activity Log is a SUBSCRIPTION log providing insight into subscription-level events that occurred in Azure.**

Through the activity log you can determine:
- **What operations were taken** on the resources in your subscription
- **Who started** the operation
- **When** the operation occurred
- The **status** of the operation
- The values of **other properties** that might help research the operation

**Activity logs are kept for 90 days.** In the portal you can **filter the Activity Log by many fields** (timespan, event category, resource group, resource, operation, severity, initiated-by, etc.).

> Exam trick: *"Who deleted the virtual machine and when?"* → **Activity Log**. *"What was the CPU utilization at 3pm?"* → **Metrics**. *"Search across all VM performance and event data with a query"* → **Log Analytics / Logs**.

### Azure Alerts

**You use Azure Monitor to configure notifications and alerts for your key systems and applications. These alerts ensure the correct team knows when a problem arises.**

**Benefits:** better notification system · **unified authoring experience** · view **Log Analytics alerts in the Azure portal** · **separation of Fired Alerts and Alert Rules** · better workflow.

**Alerts consist of three parts:**
```
Alert rules  +  Action groups  +  Monitor conditions
```

| Part | Definition |
|---|---|
| **Alert rule** | **Scope** (what resource) + **Condition/signal** (what to watch, e.g. *Delete Virtual Machine*, *Percentage CPU > 80*) + **Actions** + **Details** (name, severity, description) |
| **Action group** | **A collection of notification preferences** — email, SMS, push, voice, webhook, Logic App, Azure Function, Automation Runbook, ITSM |
| **Monitor condition** | The current state — **Fired** or **Resolved** |

**Alert states:** New / Acknowledged / Closed. **Severity: Sev 0 (critical) → Sev 4 (verbose).**

> **Lab 08 facts:** You can add **up to five action groups to an alert rule**. **Action groups are executed concurrently, in no specific order.** **Multiple alert rules can use the same action group.**

**Alert processing rules** — apply on top of fired alerts to **suppress notifications** (e.g. during a **planned maintenance window**) or to add action groups. Can run **all the time** or **at a specific time** on a schedule.

### Log Analytics

**Log Analytics is a service that helps you collect and analyze data generated by resources in your cloud and on-premises environments.** Log queries help you use the data collected in **Azure Monitor Logs**. Examples: **assessing system updates and troubleshooting operational incidents**.

**Workspace:**
- **A workspace is an Azure resource and a container where data is collected, aggregated, analyzed, and presented**
- **You can have multiple workspaces per Azure subscription**, and access to more than one workspace
- **A workspace provides a geographic location, data isolation, and scope**

**Connected sources** — the **computers and other resources that generate data collected by Log Analytics**. Includes **agents installed on Windows and Linux computers** that connect directly, or **agents in a connected System Center Operations Manager management group**. Log Analytics can also **collect data from Azure storage**.

**Data sources** — **the different data collected from each connected source**, e.g. **events and performance data from Windows and Linux agents**.

**Querying:**
- Log Analytics provides a **query syntax (KQL)** to quickly retrieve and consolidate data in the repository
- For a **quick graphical view of the health of your overall environment**, add **visualizations for saved log searches to your dashboard**
- You can **export data from the repository into tools such as Power BI or Excel**

**KQL basics (from Lab 08):**
```kusto
InsightsMetrics
| where TimeGenerated > ago(2h)
| where Name == "UtilizationPercentage"
| summarize avg(Val) by bin(TimeGenerated, 5m), Computer
| render timechart with (title = "My Chart")
```

| Operator | Purpose |
|---|---|
| `where` | Filter rows |
| `summarize` | Aggregate (`avg()`, `count()`, `max()`) |
| `bin()` | Group a timestamp into buckets (e.g. 5-minute intervals) |
| `by` | Group-by clause |
| `render` | Visualize the result (`timechart`, `barchart`, `piechart`) |
| `ago()` | Relative time (e.g. `ago(2h)`) |
| `project` | Select specific columns |
| `take` / `limit` | Return N rows |
| `sort by` / `order by` | Sort results |

Common tables: `Heartbeat` (agent check-ins), `InsightsMetrics` (VM Insights performance), `Perf`, `Event`, `Syslog`, `AzureActivity`.

### Azure Network Watcher

**A REGIONAL service that provides various network diagnostic and monitoring tools.** ⚠️ (regional — you enable it per region)

| Tool | What it does |
|---|---|
| **IP Flow Verify** | **Checks if a packet is allowed or denied to or from a virtual machine** — diagnoses connectivity issues (tells you **which NSG rule** blocked it) |
| **Next Hop** | **Determines if traffic is being correctly routed** by showing the **next hop** toward a destination |
| **Effective Security Rules** | **Details the effective inbound and outbound security rules of a VM's network interface card** (subnet + NIC NSGs combined) |
| **VPN Troubleshoot / VPN Diagnostics** | **Troubleshoots multiple gateways and connections simultaneously** |
| **Packet Capture** | **Captures inbound and outbound traffic from a virtual machine** |
| **Connection Troubleshoot** | **Checks connectivity between a source VM and a destination.** Identifies configuration issues impacting reachability; provides **all possible hop-by-hop paths**; reviews **hop-by-hop latency (min, max, average)**; views a **graphical topology** from source to destination |
| **NSG Flow Logs** | **Maps IP traffic through a network security group** — view information about **inbound and outbound IP traffic through any NSG** |
| **Topology** | **Generates a visual diagram of the resources in a virtual network and the relationships between them** |

> **Exam trick — pick the right tool:**
> - "Is my NSG blocking this packet?" → **IP Flow Verify**
> - "Which NSG rules actually apply to this VM's NIC?" → **Effective Security Rules**
> - "Is my UDR sending traffic to the NVA like I expect?" → **Next Hop**
> - "Can VM1 reach VM2 on port 3389, and what's the latency per hop?" → **Connection Troubleshoot** (this is what you used in **Lab 02**)
> - "Show me a picture of my VNet" → **Topology**
> - "Record the actual packets" → **Packet Capture**

---

## 13. Lab Recap 01–08

Short-answer questions often come straight from lab tasks. Know **what you did, why, and the key values**.

### Lab 01 — Implement Virtual Networking
**Scenario:** A global organization implementing virtual networks with capacity for growth.

| Task | What you did | Key values |
|---|---|---|
| 1 | Create a VNet with subnets **using the portal** | `CoreServicesVnet` **10.20.0.0/16**; `SharedServicesSubnet` **10.20.10.0/24**; `DatabaseSubnet` **10.20.20.0/24**. Deleted the default subnet. Then **Automation → Export template** and downloaded `template.json` |
| 2 | Create a VNet and subnets **using a template** | Edited the exported template: `CoreServicesVnet`→`ManufacturingVnet`, `10.20.0.0`→**10.30.0.0**, `SharedServicesSubnet`→`SensorSubnet1` (**10.30.20.0/24**), `DatabaseSubnet`→`SensorSubnet2` (**10.30.21.0/24**). Also edited `parameters.json`. Deployed via **Deploy a custom template → Build your own template in the editor → Load file** |
| 3 | **ASG + NSG** | Created ASG `asg-web`; created NSG `NSGSecure` and **associated it with the SharedServicesSubnet**. **Inbound rule:** Source = **Application security group** (`asg-web`), destination ports **80,443**, TCP, **Allow**, **priority 100**, name `AllowASG`. **Outbound rule:** Destination = **Service tag → Internet**, port **8080**, **Deny**, **priority 4096**. Observed the default `AllowInternetOutboundRule` at **priority 65001** that **cannot be deleted** |
| 4 | **Public and private DNS zones** | Public zone `yourName.com` — noted the **four Azure DNS name servers**; added **A record** `www` → `10.1.1.4`, **TTL 1**; verified with `nslookup www.yourName.com <name server>`. Private zone `private.yourName.com` — **no name server records**; added a **virtual network link** to `ManufacturingVnet`; added A record `sensorvm` |

**Concepts to be able to explain:** why plan address space/subnet sizes (5 reserved IPs, no re-addressing later); benefits of templates; ASG vs. NSG; public vs. private DNS zone.

### Lab 02 — Implement Inter-site Connectivity
**Scenario:** Core IT services segmented from manufacturing; they occasionally need to communicate.

| Task | What you did | Key values |
|---|---|---|
| 1–2 | Create two VMs in **two different VNets** | `CoreServicesVM` in `CoreServicesVnet` **10.0.0.0/16**, subnet `Core` **10.0.0.0/24**. `ManufacturingVM` in `ManufacturingVnet` **172.16.0.0/16**, subnet `Manufacturing` **172.16.0.0/24**. Windows Server 2025 Datacenter, **Standard_D2s_v3**, **Standard HDD** OS disk, **public inbound ports: None**, boot diagnostics disabled |
| 3 | **Network Watcher → Connection troubleshoot** | Source VM → destination VM, **TCP port 3389**. Result: **UnReachable** — *because the VMs are in different virtual networks* |
| 4 | **Configure VNet peering** | Created bidirectional peering `CoreServicesVnet-to-ManufacturingVnet` and `ManufacturingVnet-to-CoreServicesVnet`; enabled **allow access** and **allow forwarded traffic**; peering status must show **Connected** on both sides |
| 5 | **Retest with PowerShell** | On the VM: **Run command → RunPowerShellScript** → `Test-NetConnection <private IP> -port 3389`. Now **succeeds because peering is configured** |
| 6 | **Create a custom route (UDR)** | New subnet `perimeter` **10.0.1.0/24**; route table `rt-CoreServices`, **Propagate gateway routes: No**; route `PerimetertoCore`: destination **10.0.0.0/24**, **next hop type = Virtual appliance**, **next hop address 10.0.1.7**; **associated the route table with the Perimeter subnet** |

**Concepts:** peering is the cheapest/fastest VNet-to-VNet path; a UDR forces DMZ traffic through an NVA.

### Lab 03 — Implement Traffic Management
**Scenario:** Load balance public requests across VMs; serve images and videos from different VMs.

| Task | What you did | Key values |
|---|---|---|
| 1 | **Deploy infrastructure from an ARM template** | One VNet (`mst400-S64-vnet1`) with **three subnets**, one VM per subnet, one NSG. Loaded `template.json` + `parameters.json` |
| 2 | **Azure Load Balancer** (Layer 4) | **SKU Standard**, **Type Public**, **Tier Regional**. Frontend IP with a **new Standard, Regional, Static** public IP. **Backend pool** (configuration: **NIC**) with `vm0` and `vm1`. **Load balancing rule:** IPv4, TCP, **port 80 → backend port 80**, **health probe TCP port 80**, session persistence **None**, idle timeout **4** min, TCP reset **Disabled**, floating IP **Disabled**, SNAT **Recommended**. Tested by browsing the public IP and refreshing → alternates between `vm0` and `vm1` |
| 3 | **Azure Application Gateway** (Layer 7) | Added a **dedicated subnet** `subnet-appgw` **10.60.3.224/27** (*App Gateway requires a dedicated subnet of /27 or larger*). Gateway tier **Standard V2**, autoscaling **No**, instance count **2**, availability zone **1**, HTTP2 disabled. **Three backend pools:** general (nic1+nic2), **images** (nic1), **videos** (nic2). **Routing rule** priority **10**, listener **Basic**, **HTTP port 80**. **Path-based routing:** `/image/*` → images backend, `/video/*` → videos backend. Verified **Backend health = Healthy** and tested `http://<ip>/image/` and `http://<ip>/video/` |

**Concepts:** LB = L4 vs. App Gateway = L7; health probes; path-based routing; WAF purpose.

### Lab 04 — Manage Azure Storage
**Scenario:** Move infrequently accessed on-prem files to cheaper tiers; explore protection mechanisms.

| Task | What you did | Key values |
|---|---|---|
| 1 | **Create and configure a storage account** | **Standard** performance, **Geo-redundant storage (GRS)** + **"Make read access to data available in the event of regional unavailability"** (= **RA-GRS**). **Networking: Disable public access and use private access.** Data protection tab: **7 days default soft delete**, blob versioning available. Later changed public access to **Enabled from selected virtual networks and IP addresses** + **Add your client IP address** in the Firewall section. **Lifecycle management rule `Movetocool`:** if base blobs were **last modified more than 30 days ago → move to cool storage** |
| 2 | **Secure blob storage** | Created container `data` with **Private** public-access level. **Access Policy → Immutable blob storage → Add policy → Time-based retention, 180 days.** Uploaded a file: **Block blob**, **block size 4 MiB**, **access tier Hot**, upload to folder `securitytest`. Pasting the raw blob URL into an InPrivate window returned **`ResourceNotFound` / `PublicAccessNotPermitted`** — expected, since the container is Private. Then **Generate SAS**: signing key **Key 1**, permissions **Read**, start **yesterday**, expiry **tomorrow** → the **Blob SAS URL worked** in a browser |
| 3 | **Secure Azure file storage** | Created file share `share1`, access tier **Transaction optimized**, backup disabled. Used **Storage browser** to add directories and upload. Then created a VNet, added a **service endpoint for `Microsoft.Storage`** on the default subnet, added that VNet/subnet to the storage account's **Networking** blade, and **deleted your client IP from the firewall**. Result: Storage Browser returned **"not authorized to perform this operation"** because you were **not connecting from the virtual network** |

**Concepts:** GRS vs. RA-GRS; lifecycle management for cost; immutability/legal hold; SAS as delegated access; service endpoints locking storage to a VNet.

### Lab 05 — Manage Virtual Machines
**Scenario:** Compare single VMs to scale sets; configure autoscaling.

| Task | What you did | Key values |
|---|---|---|
| 1 | **Zone-resilient VMs** | Created **two VMs across Zone 1 and Zone 2** in one deployment (checked both zones, then **Edit names**). *"Availability zones offer the highest level of uptime SLA for virtual machines at **99.99%**. To achieve this SLA you must deploy at least two VMs across different availability zones."* |
| 2 | **Compute and storage scaling** | **Resized** the VM to **DS1_v2** (*resizing = vertical scaling, up or down*). Created and attached a **data disk** `vm1-disk1`, **Standard HDD, 32 GiB** → **Detached** it (*detaching removes the disk from the VM but keeps it in storage*) → changed **Size + performance** to **Standard SSD** → **reattached** it |
| 3 | **VM Scale Set** | `vmss1`, **Zones 1, 2, 3**, **Orchestration mode: Uniform**, Standard security, Windows Server 2025, **Standard D2s_v3**, **Standard HDD** OS disk. New VNet **10.82.0.0/20**, subnet `subnet0` **10.82.0.0/24**. NSG `vmss1-nsg` with inbound rule **HTTP, Allow, priority 1020**, name `allow-http`. Public IP **Enabled**. Load balancing: **Azure load balancer** → created `vmss-lb` |
| 4 | **Autoscaling** | **Custom autoscale → Scale based on metric.** **Scale-out rule:** metric **Percentage CPU**, **Greater than 10**, duration **1 minute**, statistic **Average**, **Increase count by 1**, cool down **1 minute**. **Scale-in rule:** **Less than 10**, **decrease count by 1**. **Instance limits: minimum 2, maximum 6, default 2.** Generated load with PowerShell: `$pip = (Get-AzPublicIpAddress -ResourceGroupName $rgName -Name $lbpipName).IpAddress; while ($true) { Invoke-WebRequest -Uri "http://$pip" }` |

**Concepts:** zones → 99.99%; vertical vs. horizontal scaling; why scale sets reduce admin overhead; instance limits protect against runaway scaling/cost.

### Lab 06 — Implement Web Apps & Container Apps
**Scenario:** Move PHP websites off aging on-premises Windows servers.

| Task | What you did | Key values |
|---|---|---|
| 1 | **Create an Azure web app** | Publish **Code**, **Runtime stack PHP 8.2**, **OS Linux**, region **Canada Central**. *"Azure App Services is a **Platform as a Service (PaaS)** solution... The App Service plan you select determines the web app compute, storage, and features."* |
| 2 | **Create a deployment slot** | Added slot **`staging`**, **Clone settings: Do not clone settings**. The **production** slot exists by default but isn't listed. The staging slot has **its own URL** |
| 3 | **Configure deployment settings** | On the **staging slot** → **Deployment Center → Settings → Source: External Git**, repository `https://github.com/Azure-Samples/php-docs-hello-world`, branch `master`. Staging then displays **Hello World** |
| 4 | **Swap deployment slots** | **Deployment slots → Swap → Start Swap.** Production now shows the tested code. *"Swapping a slot allows you to use the code that you tested in staging and move it to production."* |
| 5 | **Container App** | Created a Container App (region **Canada Central**) with the **quickstart image "Simple hello world container"**. *"By default the container app accepts traffic on **port 80**... Azure Container Apps provides a **DNS name** for the application."* Verified via the **Application URL** |

**Concepts:** PaaS vs. IaaS; slots eliminate downtime and give instant rollback; CI/CD from source control; Container Apps vs. AKS.

### Lab 07 — Implement Data Protection
**Scenario:** Evaluate backup/restore of Azure VMs and explore Site Recovery.

| Task | What you did | Key values |
|---|---|---|
| 1 | Deploy a VM from an **ARM template** | RG `...-rg-region1`, region **East US** |
| 2 | **Recovery Services vault + VM-level backup** | Vault in **East US** (**must be the same region as the VMs**). **Properties → Backup Configuration:** storage replication type left at **Geo-redundant** (*can only be configured if there are no existing backup items*). **Soft delete Enabled, retention 14 days.** **+ Backup** → workload running in **Azure**, back up **Virtual machine**. Policy sub types: **Enhanced** and **Standard** → chose **Standard**. New policy: **Daily**, **12:00 AM**, **Eastern Time**, **retain instant recovery snapshots for 2 days**. Added the VM → **Enable backup** → **Backup now** |
| 3 | **Monitor Azure Backup** | Created a storage account, then on the vault: **Diagnostic Settings → Add diagnostic setting** named "Logs and Metrics to storage", selected **Azure Backup Reporting Data, Addon Azure Backup Job Data, Addon Azure Backup Alert Data, Azure Site Recovery Jobs, Azure Site Recovery Events, Health**, destination **Archive to a storage account**. Then reviewed **Backup jobs** under Monitoring |
| 4 | **Enable VM replication (Site Recovery)** | Created a **second Recovery Services vault in `-rg-region2`, region West US** (**must be a different region than the VM**). On the VM: **Backup + Disaster recovery → Disaster recovery**, reviewed **Target region**, set **Churn = Normal churn** and a **cache storage account**, then **Review + Start replication → Enable replication** (10–15 min). Verified under **Protected items → Replicated items**: replication health healthy, status goes **0% → Protected** |

**Concepts:** vault region rules (backup = same region, ASR target = different region); GRS for primary/LRS for non-primary; soft delete's effect on cleanup; Backup vs. Site Recovery.

### Lab 08 — Implement Monitoring
**Scenario:** Gain insight into performance and configuration of Azure resources, especially VMs.

| Task | What you did | Key values |
|---|---|---|
| 1 | Deploy a VM from an **ARM template** | One VNet, one VM |
| 2 | **Alert + action group** | **Monitor → VM Insights → Configure Insights** → enabled on the VM (installs the agent + data collection rules). **Monitor → Alerts → Alert rule → + Create**: scope = the **resource group** (applies to any VM in it); **Condition → See all signals → "Delete Virtual Machine (Virtual Machines)"**; Event level **All**, Status **All**. **Actions → Create action group**: region **Global**, notification type **Email/SMS message/Push/Voice**, email entered. **Details:** alert rule name "VM was deleted" |
| 3 | **Trigger the alert** | Deleted the VM with **Apply force delete**. Received an email *"Important notice: Azure Monitor alert VM was deleted was activated..."* from `azure-noreply@microsoft.com`; **three verbose alerts** appeared in Monitor → Alerts |
| 4 | **Alert processing rule** | **Alerts → Alert processing rules → + Create** → scope = resource group → **Rule settings: Suppress notifications** → **Scheduling: At a specific time**, start **today 10 pm**, end **tomorrow 7 am**, local time zone → name **"Planned Maintenance"** |
| 5 | **Log queries** | **Monitor → Logs**, scope = resource group. Ran the built-in **"Count heartbeats"** query (uses the **`Heartbeat` table**), then the custom KQL query on `InsightsMetrics` rendering a **timechart** |

**Concepts:** signals vs. conditions; action groups are reusable and run concurrently; alert processing rules suppress noise during maintenance; KQL basics.

---

## 14. Master Comparison Tables

### "Which service do I choose?" — the decision table

| Requirement | Answer |
|---|---|
| Distribute TCP/UDP traffic across VMs in a region | **Azure Load Balancer** (L4) |
| Route `/images` vs `/videos` to different backends; need WAF or SSL offload | **Application Gateway** (L7) |
| Route users to the closest healthy **region** | **Traffic Manager** (DNS) |
| Force subnet traffic through a firewall appliance | **UDR / route table** with next hop **Virtual appliance** |
| Filter traffic to/from a subnet or NIC with simple rules | **NSG** |
| Group VMs by app role so rules don't need IPs | **Application Security Group** |
| Centralized, stateful, FQDN-filtering firewall across VNets/subscriptions | **Azure Firewall** |
| Lock a storage account to a specific subnet, free | **Service endpoint** |
| Give a PaaS service a private IP inside the VNet, reachable from on-prem | **Private Endpoint / Private Link** |
| Connect two VNets, low latency, no gateway | **VNet peering** |
| Connect on-premises to Azure over the internet, encrypted | **Site-to-site VPN** |
| Connect a single laptop to a VNet | **Point-to-site VPN** |
| Private, high-bandwidth, non-internet link to Azure + Microsoft 365 | **ExpressRoute** |
| Protect against accidental resource deletion | **Resource lock (Delete/CanNotDelete)** |
| Enforce "only these VM sizes may be deployed" | **Azure Policy** |
| Give a user rights to manage resources but not grant access | **RBAC: Contributor** |
| Restore a deleted file from a Windows server | **Azure Backup / MARS agent** |
| Fail an entire region's VMs over to another region | **Azure Site Recovery** |
| See who deleted a resource | **Activity Log** |
| Chart CPU over the last hour | **Metrics (Azure Monitor)** |
| Query VM performance & event data with KQL | **Log Analytics** |
| Find out which NSG rule blocked a packet | **Network Watcher → IP Flow Verify** |
| Test end-to-end reachability and latency between two VMs | **Network Watcher → Connection Troubleshoot** |
| Test a new app version without downtime, then roll back instantly | **Deployment slots + swap** |
| Run a container without managing VMs or an orchestrator | **Azure Container Instances / Container Apps** |
| Store files that many VMs mount as a drive over SMB | **Azure Files** |
| Store images/video streamed to browsers at massive scale | **Blob storage** |
| Archive data accessed once a year, cheapest storage | **Archive tier** (min 180 days, hours to retrieve) |

### Storage: which tier / which redundancy

```
Access frequency:     Hot ──────► Cool (30d min) ──────► Archive (180d min, hours to rehydrate)
Storage cost:         high  ────────────────────────────►  low
Access cost:          low   ────────────────────────────►  high

Redundancy:           LRS (3, 1 region)
                       ├─ zone protection ──► ZRS (3 zones)
                       ├─ region protection ► GRS (6, 2 regions)  ──► + read = RA-GRS
                       └─ both ─────────────► GZRS (6, 3+1 zones) ──► + read = RA-GZRS
```

### Availability: sets vs. zones

| | **Availability Set** | **Availability Zone** |
|---|---|---|
| Protects against | Rack/hardware failure and **planned maintenance** within a datacenter | **Entire datacenter** failure |
| Mechanism | **Fault domains + update domains** | **Physically separate datacenters** with independent power, cooling, networking |
| SLA (2+ VMs) | **99.95%** | **99.99%** |
| Scope | Within one datacenter | Within one region (min 3 zones) |

---

## 15. PowerShell / CLI Command Sheet

### Groups & identity
```powershell
New-AzADGroup -DisplayName Developers -MailNickname Developers
Get-AzADGroup
Get-AzADUser
Add-AzADGroupMember -MemberUserPrincipalName "me@domain.com" -TargetGroupDisplayName "MyGroup"
Get-AzADGroupMember -GroupDisplayName "MyGroup"
```

### Resource groups & locks
```powershell
Get-AzResourceGroup
Remove-AzResourceGroup -Name "<rgName>" -Force -AsJob
New-AzResourceLock -LockName <lockName> -LockLevel CanNotDelete -ResourceGroupName <rgName>
Get-AzResourceLock
Remove-AzResourceLock -LockName <name> -ResourceGroupName <rg>
```

### Virtual networking
```powershell
$vnet = New-AzVirtualNetwork -ResourceGroupName demo-RG -Location EastUS -Name myVNet2 -AddressPrefix 10.0.0.0/16
Get-AzVirtualNetwork -Name myVNet2
$subnet = Add-AzVirtualNetworkSubnetConfig -Name mySubnet2 -AddressPrefix 10.0.0.0/24 -VirtualNetwork $vnet
Get-AzVirtualNetworkSubnetConfig -Name mySubnet2 -VirtualNetwork $vnet
$subnet | Set-AzVirtualNetwork          # commit
Get-AzEffectiveRouteTable                # view routing information
```

### Virtual machines
```powershell
New-AzVm -ResourceGroupName "Demo-RG" -Name "Demo-VM" -Image "UbuntuLTS"
Test-NetConnection <private IP> -port 3389      # run inside a VM (Run command → RunPowerShellScript)
Get-AzPublicIpAddress -ResourceGroupName $rg -Name $lbpipName
```

### Load generation (Lab 05)
```powershell
$pip = (Get-AzPublicIpAddress -ResourceGroupName $rgName -Name $lbpipName).IpAddress
while ($true) { Invoke-WebRequest -Uri "http://$pip" }
```

### Help
```powershell
Get-Verb                                  # approved PowerShell verbs
Get-Help Get-ChildItem -detailed          # help for any cmdlet
```

### Azure CLI
```bash
az vm restart -g MyResourceGroup -n MyVm
az find "az vm"                            # find/help
```

### Verb–noun pattern
Azure PowerShell = **`<Verb>-Az<Noun>`**. Verbs: `New` (create), `Get` (read), `Set` (update), `Remove` (delete), `Add`, `Update`, `Start`, `Stop`, `Restart`.

---

## 16. Practice Exam — Multiple Choice

Answer all 45, then check the key at the end. Aim for 40+.

**1.** How many IP addresses does Azure reserve in every subnet?
A) 3 B) 4 C) 5 D) 6

**2.** A resource group tagged `Environment=Prod` contains 10 VMs. How many VMs have that tag?
A) All 10 B) 0 C) Only new ones D) Depends on Azure Policy

**3.** Which two lock types does Azure Resource Manager support?
A) Write and Delete B) ReadOnly and Delete C) Full and Partial D) CanNotWrite and CanNotDelete

**4.** Which roles can create or delete management locks?
A) Contributor and Owner B) Owner and User Access Administrator C) Reader and Owner D) Any role with write permission

**5.** Which NSG rule is evaluated first: priority 200 or priority 4000?
A) 4000 B) 200 C) Both simultaneously D) Whichever is on the NIC

**6.** For inbound traffic to a VM, which NSG is evaluated first?
A) The NIC NSG B) The subnet NSG C) Whichever has lower priority D) Azure Firewall

**7.** Azure Firewall processes rules in what order?
A) Application → Network → NAT B) Network → NAT → Application C) NAT → Network → Application D) All simultaneously

**8.** Which Azure Firewall rule type would you use to allow outbound traffic to `*.microsoft.com` over HTTPS?
A) NAT rule B) Network rule C) Application rule D) DNAT rule

**9.** What must the VPN gateway subnet be named?
A) VPNSubnet B) GatewaySubnet C) AzureGatewaySubnet D) Any name is fine

**10.** VNet A is peered to VNet B, and VNet B is peered to VNet C. Can resources in A reach C?
A) Yes, automatically B) No — peering is non-transitive C) Only with gateway transit D) Only if in the same region

**11.** Which is Layer 7?
A) Azure Load Balancer B) Application Gateway C) Both D) Neither

**12.** An Application Gateway requires a dedicated subnet of at least what size?
A) /24 B) /28 C) /27 D) /29

**13.** How many route tables can be associated with a single subnet?
A) Unlimited B) Up to 5 C) One D) One per next hop type

**14.** Which blob type is used for Azure VM OS and data disks?
A) Block blob B) Append blob C) Page blob D) Managed blob

**15.** Which blob type is optimized for logging?
A) Block blob B) Append blob C) Page blob D) Table blob

**16.** Can a blob's type be changed after creation?
A) Yes B) No C) Only within 30 days D) Only for block blobs

**17.** Minimum storage duration for the Archive tier?
A) 30 days B) 90 days C) 180 days D) 365 days

**18.** Which redundancy option provides 6 replicas across 2 regions with read access to the secondary?
A) GRS B) RA-GRS C) ZRS D) LRS

**19.** Which redundancy option writes synchronously to three zones AND asynchronously to a secondary region?
A) GRS B) ZRS C) GZRS D) RA-GRS

**20.** Storage Service Encryption uses which algorithm and can it be disabled?
A) 128-bit AES, yes B) 256-bit AES, no C) 256-bit RSA, yes D) 512-bit AES, no

**21.** What is the SLA for two or more VMs deployed across two or more availability zones?
A) 99.9% B) 99.95% C) 99.99% D) 99.999%

**22.** What is the SLA for two or more VMs in an availability set?
A) 99.9% B) 99.95% C) 99.99% D) None

**23.** By default, how many update domains does an availability set have?
A) 2 B) 3 C) 5 D) 20

**24.** Which disk on an Azure VM should NOT be used to store data you need to keep?
A) OS disk B) Data disk C) Temporary disk D) Managed disk

**25.** How many deployment slots does the Standard App Service tier support?
A) 0 B) 5 C) 10 D) 20

**26.** Which App Service tiers support backup?
A) Free and Shared B) Basic and above C) Standard and Premium D) All tiers

**27.** Max size of an App Service backup?
A) 1 GB B) 5 GB C) 10 GB D) 100 GB

**28.** "Scale out" for a web app means:
A) Change the pricing tier B) Increase the number of VM instances C) Add more disk D) Move to another region

**29.** What is a container group?
A) A Kubernetes namespace B) A collection of containers scheduled on the same host machine C) A container registry D) A Docker image layer

**30.** Which statement about container isolation is true?
A) Containers isolate better than VMs B) VMs provide a stronger security boundary than containers C) They are identical D) Containers run their own kernel

**31.** How long are backups preserved in soft-delete state after deletion?
A) 7 days B) 14 days C) 30 days D) 90 days

**32.** How long is the Azure Activity Log retained?
A) 30 days B) 60 days C) 90 days D) 1 year

**33.** By default, how long are VM backup instant-restore snapshots retained, and what is the configurable range?
A) 1 day, 1–7 B) 2 days, 1–5 C) 5 days, 1–10 D) 7 days, 1–14

**34.** Which limitation applies to the MARS agent?
A) Requires a separate backup server B) Not application aware; file, folder, and volume-level restore only C) Cannot back up Windows D) Requires System Center

**35.** Which backup component can back up VMware VMs and provides app-aware snapshots?
A) MARS agent B) Azure Backup Server (MABS) C) Azure Site Recovery D) Managed disk snapshots

**36.** You need to recover from an entire Azure region going offline. Which service?
A) Azure Backup B) Azure Site Recovery C) Managed disk snapshots D) Soft delete

**37.** Which Network Watcher tool tells you whether a packet is allowed or denied to/from a VM?
A) Next Hop B) Topology C) IP Flow Verify D) Packet Capture

**38.** Which Network Watcher tool shows hop-by-hop latency between a source VM and a destination?
A) IP Flow Verify B) Connection Troubleshoot C) NSG Flow Logs D) Effective Security Rules

**39.** Azure Monitor data falls into which two fundamental types?
A) Alerts and actions B) Metrics and logs C) Events and traces D) Signals and conditions

**40.** How many action groups can be attached to a single alert rule?
A) 1 B) 3 C) 5 D) Unlimited

**41.** In Entra ID, which feature requires a P2 license?
A) MFA B) Conditional Access C) Privileged Identity Management (PIM) D) Self-service password reset

**42.** Which membership type is available only for security groups (not Microsoft 365 groups)?
A) Assigned B) Dynamic User C) Dynamic Device D) Nested

**43.** A user's Source in Entra ID shows "Windows Server AD". What type of user is this?
A) Cloud identity B) Directory-synchronized identity C) Guest user D) Service principal

**44.** Which record types can verify a custom domain name in Entra ID?
A) A or CNAME B) MX or TXT C) NS or SOA D) SRV or PTR

**45.** Which two things does an Azure Cloud Shell session require?
A) A VM and a public IP B) A storage account and an Azure File share (plus a resource group) C) A VNet and an NSG D) Nothing — it's fully serverless

### Answer key
1-C · 2-B · 3-B · 4-B · 5-B · 6-B · 7-C · 8-C · 9-B · 10-B · 11-B · 12-C · 13-C · 14-C · 15-B · 16-B · 17-C · 18-B · 19-C · 20-B · 21-C · 22-B · 23-C · 24-C · 25-B · 26-C · 27-C · 28-B · 29-B · 30-B · 31-B · 32-C · 33-B · 34-B · 35-B · 36-B · 37-C · 38-B · 39-B · 40-C · 41-C · 42-C · 43-B · 44-B · 45-B

---

## 17. Practice Short-Answer Questions

Write your answer first, then compare. Short-answer graders want **the key terms**, so I've **bolded** the words worth earning marks for.

**Q1. Explain the difference between an Azure tenant and an Azure subscription.**
A **tenant (directory)** is a **dedicated, trusted instance of Microsoft Entra ID representing a single organization** — the **identity boundary**. It's created **automatically** when an organization signs up for a Microsoft cloud service, and it holds users, groups, and app registrations. An **Azure subscription** is a **logical container used to provision and manage Azure resources** and is the **unit of management, billing, and scale** — it's how you **pay for** Azure services. A subscription trusts exactly one tenant, but one tenant can have **many subscriptions** (e.g. production, Dev/Test, sandbox).

**Q2. List three differences between Microsoft Entra ID and Windows Server Active Directory Domain Services.**
1. Entra ID is queried using a **REST API over HTTP/HTTPS**, while AD DS uses **LDAP**.
2. Entra ID authenticates with **SAML, WS-Federation, and OpenID Connect** (and **OAuth for authorization**); AD DS uses **Kerberos/NTLM**.
3. Entra ID users and groups are in a **flat structure — there are no Organizational Units (OUs) or Group Policy Objects (GPOs)**; AD DS is hierarchical with OUs, GPOs, domains, and forests.
(Bonus: Entra ID is **primarily an identity solution** and includes **federation services and third-party services** such as Facebook.)

**Q3. What is a resource group, and name three rules that govern it.**
A resource group is a **logical container that holds related resources**. Rules: (1) **All resources in a group should share the same lifecycle** — deploy, update, and delete them together; (2) **a resource can exist in only one resource group**; (3) **resource groups cannot be renamed**; (4) a group **can contain many resource types and resources from many different regions**.

**Q4. Why does a /24 subnet in Azure only give you 251 usable addresses?**
Because **Azure reserves five IP addresses in every subnet**: **`x.0`** (network address), **`x.1`** (Azure default gateway), **`x.2` and `x.3`** (reserved to map the **Azure DNS IPs** into the VNet space), and **`x.255`** (network broadcast address). 256 − 5 = **251**.

**Q5. Explain how NSGs are evaluated when a subnet NSG and a NIC NSG are both present.**
**NSGs are evaluated independently and an "allow" rule must exist at BOTH levels** for traffic to pass. For **inbound** traffic, the **subnet** NSG is evaluated **first**, then the **NIC** NSG. For **outbound** traffic it is the **reverse** — **NIC first, then subnet**. Within each NSG, rules are processed **in priority order, lowest number first**, and processing stops at the first match. Use the **Effective security rules** view to see the combined result.

**Q6. What is the difference between an NSG and an ASG?**
An **NSG** is a set of **security rules that allow or deny inbound/outbound traffic**, attached to a **subnet or a NIC** (zero or one each). An **ASG** is a **logical grouping of network interfaces by application role** (e.g. web servers). The ASG contains **no rules itself** — you reference it **as the source or destination inside an NSG rule**, so you never have to hard-code or maintain IP addresses as VMs are added or removed.

**Q7. Describe the three Azure Firewall rule types and the order in which they are processed.**
**NAT (DNAT) rules** translate and filter **inbound** traffic — they translate the firewall's **public IP and port to a private IP and port**; a **NAT rule must be matched by a network rule** for traffic to pass. **Network rules** handle **any non-HTTP/S traffic** and subnet-to-subnet communication, filtering by **protocol (TCP/UDP/ICMP/Any), source address, destination addresses, and destination ports**. **Application rules** define **FQDNs that can be accessed from a subnet** over HTTP/HTTPS, supporting **wildcards and FQDN tags** (e.g. Windows Update, Azure Backup). Processing order: **NAT → Network → Application**, and **once a rule allows the traffic through, no more rules are checked**. **By default Azure Firewall blocks all traffic.**

**Q8. Explain VNet peering and why service chaining is needed.**
**VNet peering** connects two virtual networks so resources can communicate. Traffic is **private, stays on the Microsoft backbone**, requires **no public internet, gateways, or encryption**, offers **low latency and high bandwidth**, works **across subscriptions, deployment models, and regions**, and causes **no downtime** to create. However, **peering is non-transitive** — if A↔B and B↔C are peered, A cannot reach C. To provide transitivity you configure **user-defined routes and service chaining**, directing traffic to the **IP address of a virtual appliance in a peered VNet or a VPN gateway as the next hop**. This enables a **multi-level hub-and-spoke architecture** and helps **overcome the limit on the number of peerings per VNet**. Address spaces of peered VNets **must not overlap**.

**Q9. Compare Azure Load Balancer with Azure Application Gateway.**
**Azure Load Balancer** operates at **Layer 4** (TCP/UDP). A **public** load balancer **maps the public IP address and port of incoming traffic to the private IP address and port of the VM**, and provides the mapping for **response traffic** as well; an **internal** load balancer uses only private IPs. It is configured with a **frontend IP, backend pool, load balancing rules, and health probes**. **Application Gateway** operates at **Layer 7** (HTTP/HTTPS) and adds **URL path-based routing, multi-site hosting, SSL/TLS termination and end-to-end encryption, a Web Application Firewall (WAF), cookie-based session affinity, and connection draining**. Its flow is **frontend IP → listener → rule → backend instances**, and it needs a **dedicated subnet of /27 or larger**.

**Q10. What are user-defined routes and what are the constraints?**
**UDRs control network traffic by defining the next hop of the traffic flow.** The next hop can be a **virtual network gateway, virtual network, internet, or virtual appliance** (and `None` to drop traffic). **A route table can be associated with multiple subnets, but a subnet can only be associated with a single route table.** **There is no charge for creating route tables.** UDRs **override Azure's default system routes**. The steps are: **create the route table → create the custom route → associate the route table with the subnet**.

**Q11. Compare service endpoints with private endpoints.**
A **service endpoint provides an identity to your virtual network** for an Azure service. Benefits: **improved security for Azure service resources, optimal routing for Azure service traffic, traffic goes directly from your VNet to the service on the Microsoft backbone, and it's simple to set up with less management overhead**. Traffic still targets the service's **public endpoint**, and the endpoint **cannot be used from on-premises or peered networks**. A **Private Link/private endpoint brings the service into your private virtual network by mapping it to a private endpoint, eliminating data exposure to the public internet**. It provides **private connectivity, integration with on-premises and peered networks, protection against data exfiltration, and delivery of services directly to customers' virtual networks** — and it gives the service a **private IP inside your VNet**.

**Q12. Compare the six Azure Storage redundancy options.**
**LRS** — **three replicas in one region**; protects against **disk, node, and rack failures**; the write is acknowledged **when all replicas are committed**. **ZRS** — **three replicas across three zones in one region**, **synchronous** writes; adds **zone failure** protection. **GRS** — **six replicas across two regions (three per region)**, **asynchronous** copy to the secondary; protects against **major regional disasters**. **RA-GRS** — GRS plus **read access to the secondary** via a **separate secondary endpoint**; the **RPO delay can be queried**. **GZRS** — **six replicas, 3+1 zones, two regions**; **synchronous** to three zones plus **asynchronous** to the secondary; protects against disk, node, rack, **zone, and region** failures. **RA-GZRS** — GZRS plus read access to the secondary.

**Q13. Explain the three blob access tiers and the cost tradeoff.**
**Hot** = frequent access. **Cool** = infrequent access, **stored for at least 30 days**. **Archive** = rarely accessed, **stored for at least 180 days**, with **several hours of retrieval latency**. **You can switch access tiers at any time.** The tradeoff: **as the tier gets cooler, the per-gigabyte storage cost decreases, but data access and transaction costs increase** — and **changing the storage tier itself incurs a charge**.

**Q14. What is a Shared Access Signature and list four best practices for using one.**
A **SAS is a URI that grants restricted access rights to Azure Storage resources** — a **signed URI** made of your **storage resource URI plus the SAS token**, with parameters for **services, resource types, start time, expiry time, resource, permissions, IP range, protocol, and signature**. Best practices: **always use HTTPS** to create/distribute a SAS; **reference stored access policies where possible**; use **near-term expiration times** on unplanned SAS; **have clients automatically renew** the SAS; **be careful with the SAS start time**; **be specific with the resource** being accessed; understand **your account is billed for any usage including via SAS**; **validate data written using a SAS**; and **use Storage Analytics to monitor**.

**Q15. Name and describe the six Azure File Sync components.**
**Storage Sync Service** — the **top-level resource**. **Registered server** — represents the **trust relationship between your server (or cluster) and the Storage Sync Service**. **Azure File Sync agent** — the **downloadable package** that enables Windows Server to sync with an Azure file share. **Server endpoint** — a **specific location on a registered server, such as a folder**. **Cloud endpoint** — **an Azure file share**. **Sync group** — **defines which files are kept in sync**.

**Q16. What are availability sets, update domains, and fault domains?**
An **availability set prevents a single point of failure** for VMs; the VMs in it should **perform an identical set of functions and have the same software installed**, each application tier should be in its **own availability set**, and it should be **combined with a load balancer** using **managed disks**. An **update domain** groups VMs that are rebooted together during **planned maintenance** — **only one update domain is rebooted at a time**; there are **five by default (non-user-configurable at that default), configurable up to 20**. A **fault domain** groups VMs that **share a common set of hardware and switches — a single point of failure**, such as a **server rack** with shared power and networking.

**Q17. What are Azure deployment slots and why use them?**
Deployment slots are **live apps with their own hostnames** that let you **deploy to a non-production slot and validate changes before sending them to production**. Swapping **avoids a cold start and eliminates downtime**, and lets you **fall back to a last known good site**. **Auto Swap** is available when pre-swap validation isn't needed. Slot availability by tier: **Free/Shared/Basic = 0, Standard = up to 5, Premium and Isolated = up to 20**. New slots can be **empty or cloned**, and settings fall into three categories: **slot-specific app settings and connection strings, continuous deployment settings, and App Service authentication settings**. Note that **not all settings are sticky** — endpoints, custom domain names, SSL certificates, and scaling move with the swap.

**Q18. Compare containers and virtual machines.**
**Isolation:** containers provide **lightweight isolation but not as strong a security boundary as a VM**; VMs provide **complete isolation from the host OS and other VMs**, which matters when hosting apps from **competing companies** on the same cluster. **OS:** a container runs only the **user mode portion** of an OS and can be tailored to just the needed services, **using fewer system resources**; a VM runs a **complete OS including the kernel**, requiring more CPU, memory, and storage. **Deployment:** containers deploy individually with **Docker via the command line** or in bulk via an **orchestrator such as AKS**; VMs deploy via **Windows Admin Center/Hyper-V Manager** or **PowerShell/System Center VMM**. **Persistent storage:** containers use **Azure Disks** (single node) or **Azure Files/SMB** (shared); VMs use a **VHD** or an **SMB file share**. **Fault tolerance:** containers are **rapidly recreated by the orchestrator on another node**; VMs **fail over to another server in a cluster with the OS restarting**.

**Q19. Contrast Azure Backup with Azure Site Recovery.**
**Azure Backup** protects against **data loss** — accidental or malicious deletion and corruption. It takes **recovery points** at scheduled intervals and stores them in a **Recovery Services vault**; it supports **application-consistent backups for Windows and Linux VMs**, and you **restore** individual items or whole VMs. **Azure Site Recovery** protects against **a major disaster when a whole region experiences an outage**. It **replicates workloads from a primary site to a secondary location**, you **fail over** with a single click and later **fail back**. Scenarios include **Azure region → Azure region**, **on-premises VMware/Hyper-V/physical/Azure Stack → Azure**, **AWS Windows instances → Azure**, and **on-premises → a secondary on-premises site**.

**Q20. Compare the MARS agent with Azure Backup Server (MABS).**
**MARS agent:** backs up **files and folders on physical or virtual Windows machines**; **no separate backup server required**; limits are **3 backups per day**, **not application aware**, **file/folder/volume-level restore only**, and **no Linux support**. It protects **files and folders**, storing them in a **Recovery Services vault**. **MABS/DPM:** provides **app-aware snapshots** (SQL Server, Exchange, SharePoint), **full flexibility on backup timing**, **recovery granularity**, **Linux support on Hyper-V and VMware VMs**, and can **back up and restore VMware VMs** without a System Center license. Limits: **cannot back up Oracle workloads**, **always requires a live Azure subscription**, and **no tape backup support**. It protects **files, folders, volumes, VMs, applications, and workloads**, storing to a **Recovery Services vault and locally attached disk**.

**Q21. Explain the difference between metrics and logs in Azure Monitor, and give an example question each answers.**
**Metrics are numerical values that describe some aspect of a system at a particular point in time** — lightweight and capable of supporting **near real-time** scenarios (e.g. *"What was the VM's CPU percentage at 3:00 pm?"*). **Logs contain different kinds of data organized into records with different sets of properties for each type**; events and traces are stored as logs **in addition to performance data so it can all be combined for analysis**, and they're queried with **KQL in Log Analytics** (e.g. *"Show me every VM whose disk utilization exceeded 90% in the last 24 hours, by computer"*). **All data collected by Azure Monitor fits into one of these two fundamental types.**

**Q22. Name five Network Watcher diagnostic tools and what each does.**
**IP Flow Verify** — checks **if a packet is allowed or denied to or from a virtual machine**. **Next Hop** — determines **whether traffic is being routed to the intended destination** by showing the next hop. **Effective Security Rules** — details the **effective inbound and outbound security rules of a VM's NIC**. **VPN Troubleshoot** — troubleshoots **multiple gateways and connections simultaneously**. **Packet Capture** — **captures inbound and outbound traffic from a VM**. **Connection Troubleshoot** — checks **connectivity between a source VM and a destination**, identifies configuration issues, provides **hop-by-hop paths and latency**, and shows a graphical topology. **NSG Flow Logs** — shows **inbound and outbound IP traffic through any NSG**. **Topology** — generates a **visual diagram of VNet resources and their relationships**.

**Q23. In Lab 02, Connection Troubleshoot reported "UnReachable" before you configured peering. Explain why, and what changed after.**
The two VMs were in **separate virtual networks** (`CoreServicesVnet` 10.0.0.0/16 and `ManufacturingVnet` 172.16.0.0/16). **Azure routes traffic between subnets within a VNet by default, but separate VNets are isolated** — there was **no route and no connectivity** between them, so the TCP 3389 test failed. After creating a **bidirectional VNet peering** (with *allow access* and *allow forwarded traffic* enabled on both links, status **Connected**), the VNets could communicate **privately over the Microsoft backbone**, and `Test-NetConnection <private IP> -port 3389` succeeded.

**Q24. In Lab 04, after adding a service endpoint you could no longer browse your file share from Storage Browser. Why?**
You added a **`Microsoft.Storage` service endpoint** on the VNet's default subnet, added that **VNet/subnet to the storage account's Networking blade**, and then **removed your client IP from the storage firewall**. The storage account was then configured to **only accept traffic originating from that virtual network**. Because the portal's Storage Browser connects from **your workstation's public IP — not from inside the VNet** — the request was rejected with **"not authorized to perform this operation."**

**Q25. Describe the steps to implement a site-to-site VPN connection.**
1. **Create the VNets and subnets** (for S2S you connect to an on-premises location). 2. **Optionally specify a DNS server** if you need name resolution for resources in the VNet. 3. **Create the gateway subnet** — it holds the IP addresses used by the virtual network gateway, should be **`/27` or `/28`**, **must be named `GatewaySubnet`**, and must **never contain other resources**. 4. **Create the VPN gateway** — choose the **VPN type (route-based)** based on your VPN device make/model, choose a **SKU** (which determines the **number of tunnels and aggregate throughput**), associate the VNet containing the gateway subnet, and assign a **public IP**. 5. **Create the local network gateway**, representing the on-premises site — its **public IP or FQDN** and its **address space in CIDR notation**. 6. **Create the VPN connection** between the gateways and verify it **in the portal or with PowerShell**. High availability options are **Active/Standby** and **Active/Active**.

---

## 18. Night-Before Checklist & Exam Strategy

### The 15 facts to review in the hallway
1. **5 reserved IPs** per subnet: `.0` network, `.1` gateway, `.2`/`.3` DNS, `.255` broadcast
2. **SLAs: 99.99% zones · 99.95% availability set · 99.9% single VM w/ premium storage**
3. **NSG:** subnet first inbound, NIC first outbound, **allow needed at both levels**, **lower priority number wins**
4. **Firewall: NAT → Network → Application**, denies everything by default
5. **Peering is non-transitive**; address spaces can't overlap; **GatewaySubnet** is the required name
6. **LB = L4 · App Gateway = L7 (/27 subnet, WAF, path routing) · Traffic Manager = DNS/global**
7. **Subnet → one route table.** Route tables are free.
8. **Blob tiers: Hot / Cool (30d) / Archive (180d).** Blob **type** can't change; **tier** can.
9. **LRS 3/1 · ZRS 3 zones · GRS 6/2 · add RA- for read access to secondary**
10. **Block (default) / Append (logs) / Page (VM disks, 8 TB)**
11. **Slots: Free-Shared-Basic 0 · Standard 5 · Premium/Isolated 20.** Backup needs **Standard or Premium**, max **10 GB**
12. **Soft delete 14 days · Activity Log 90 days · snapshot retention 2 days (1–5)**
13. **Backup = data loss. Site Recovery = region outage (fail over / fail back).**
14. **Tags: max 50, NOT inherited. Locks: ReadOnly/Delete, ARE inherited, Owner + UAA only.**
15. **Entra P2 = PIM + risk-based Conditional Access. P1 = Conditional Access, advanced groups, Administrative Units.**

### Exam strategy (80 minutes, 29 questions)
- **Budget:** ~2 min per multiple choice, ~5 min per short answer. Take **one fast pass** answering everything you're sure of, then return to the rest.
- **Multiple choice:** eliminate first. Watch for absolute words ("always", "never", "cannot") — in Azure, the true absolutes are things like *"SSE cannot be disabled"*, *"blob type cannot be changed"*, *"tags are not inherited"*, *"peering is non-transitive"*, *"resource groups cannot be renamed"*.
- **Short answer:** lead with the **definition sentence**, then give **specific named features/numbers**. Graders scan for keywords — write **"non-transitive"**, **"Layer 7"**, **"GatewaySubnet"**, **"99.99%"**, **"180 days"**, not paraphrases.
- If a question describes a **lab scenario** (peering test, load balancer path routing, SAS URL, backup vault region, alert action group), answer with **what you actually configured and why** — that's what these questions are testing.
- If you blank on a service, ask: **what layer does it work at? what is it protecting against? is it regional or global?** That usually narrows it to one answer.

Good luck Thursday. 🎯
