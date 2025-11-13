# 🐡🐠🐟🐳🐋🦪🪼🐙🦑🦀🦞🐧🦭🐬🪸🦈

# Citrouille User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Common Use Cases](#common-use-cases)
3. [Command Reference](#command-reference)
4. [Configuration File](#configuration-file)
5. [Reporting Issues](#reporting-issues)



## Introduction

Citrouille is a command-line tool designed to help you manage and secure your Kubernetes deployments without requiring deep Kubernetes expertise. It provides three main capabilities:

- **Inventory:** Identify deployments within a namespace
- **Compare:** Compare deployments between different namespaces
- **Security:** Identify security issues and misconfigurations within a namespace

### Target audience

Citrouille targets:
- Delivery managers and product owners handling multiple Kubernetes environments
- DevOps engineers seeking to audit their Kubernetes deployments
- Developers who need to check deployment status without learning Kubernetes in depth
- Teams performing blue/green deployments or canary releases



## Common Use Cases

### 1. Daily Deployment Monitoring

Check what's running in production every morning:

```bash
$ citrouille inventory production
```

### 2. Pre-Deployment Verification

Before promoting staging to production, verify they match:

```bash
$ citrouille compare staging production
```

### 3. Blue/Green Deployment Validation

After deploying to the "green" environment, compare with "blue":

```bash
$ citrouille compare blue green
```

### 4. Security Audit Before Release

Run security checks before releasing to production:

```bash
$ citrouille security staging
```



## Command Reference

### Global Options

```bash
--kubeconfig PATH    Path to your kubeconfig file (default: ~/.kube/config)
--context NAME       Kubernetes context to use (default: current context)
-o, --output FORMAT  Output format: table or json (default: table)
--version            Show version information
--help               Show help message
```

**Examples:**

```bash
citrouille --kubeconfig /path/to/config inventory

citrouille --context production inventory

citrouille -o json inventory
```



### Inventory Command

View deployments in a namespace.

**Syntax:**
```bash
citrouille inventory [NAMESPACE] [OPTIONS]
```

**Options:**
- `NAMESPACE`              # Target namespace (default: `default`)
- `-A, --all-namespaces`   # List deployments across all namespaces

**Examples:**

```bash
# View deployments in default namespace
$ citrouille inventory

# View deployments in production namespace
$ citrouille inventory production

# View deployments in all namespaces
$ citrouille inventory -A

# Get JSON output for production
$ citrouille -o json inventory production
```

**Sample Output:**

```bash
$ citrouille inventory
NAME                   NAMESPACE  IMAGES                                                                                  CREATED              REPLICAS
-------------------------------------------------------------------------------------------------------------------------------------------------------
adservice              default    adservice:7b941b6a77efd8128a4926cfc44fa56beee5c8a3cb5a210b17e8b6c3bff71bd3              2025-11-11 00:35:52  1       
cartservice            default    cartservice:57c0f36f4ab71151f828c00e4e63c5845b1ede392ca3537c78db4c95372978e0            2025-11-11 00:35:52  1       
checkoutservice        default    checkoutservice:0bfca777c38c87f4f01856cbefa8b3cb2789ea733795c99deaa187caa10fe2eb        2025-11-11 00:35:52  1       
currencyservice        default    currencyservice:cf4a11ba0955181a90227cebf24894617e07708f6562249adac1c13dc9201c7c        2025-11-11 00:35:52  1       
emailservice           default    emailservice:af249f73cb356ea676d39139a3f2a1e6b890276193b80fb5cd1667c9d9be53a4           2025-11-11 00:35:52  1       
frontend               default    frontend:639a6cea6a28452c81c6f73664ba5cc44e8586da9871ac7054c8d21cbb92ce3a               2025-11-11 00:35:52  1       
loadgenerator          default    loadgenerator:03ae10cd99c0484936bfa8492f6f577d59071fdf25b3259a034881674cc2f829          2025-11-11 00:36:25  1       
paymentservice         default    paymentservice:5c1e579ed7e765f8e6bc018297b47008abf8b6783dac3dc322de0f641acd8436         2025-11-11 00:35:52  1       
productcatalogservice  default    productcatalogservice:9eaa4acd1ed815af7959acc4ff930ddc91828d5153a3672cfe5329b7b5c48306  2025-11-11 00:35:52  1       
recommendationservice  default    recommendationservice:8846d556ce9a7ad1a93f71b4bde6668b9621968c5da3c1d5432f30b1bb1d808f  2025-11-11 00:35:52  1       
redis-cart             default    redis:alpine                                                                            2025-11-11 00:35:52  1       
shippingservice        default    shippingservice:5c5913794444085bb1493023b68df8b2f16a22c2472dfd5e40c81db0d223eb8d        2025-11-11 00:35:52  1
```

---

### Compare Command

Compare deployments between two namespaces to identify differences.

**Syntax:**
```bash
$ citrouille compare NAMESPACE1 NAMESPACE2 [OPTIONS]
```

**Arguments:**
- `NAMESPACE1` - First namespace (source)
- `NAMESPACE2` - Second namespace (target)

**Examples:**

```bash
# Compare production and staging
$ citrouille compare production staging

# Compare with JSON output
$ citrouille -o json compare production staging

# Compare using namespace aliases (requires config file)
$ citrouille compare prod stg
```

**Sample Output:**

```bash
$ citrouille compare prod dev

Comparing namespaces: 'default' vs 'dev'

================================================================================

[-] Missing in 'dev' (1 deployment(s)):
--------------------------------------------------------------------------------
  Name:     adservice
  Images:   adservice:7b941b6a77efd8128a4926cfc44fa56beee5c8a3cb5a210b17e8b6c3bff71bd3
  Replicas: 1

================================================================================
Summary: 1 missing, 0 extra, 0 changed
```

### Security Command

Perform security analysis on deployments to identify misconfigurations and vulnerabilities.

**Syntax:**
```bash
$ citrouille security [NAMESPACE] [OPTIONS]
```

**Options:**
- `NAMESPACE` - Target namespace (default: `default`)
- `--check-config` - Run configuration security checks only
- `--check-network` - Run network security checks only
- If no specific check is specified, all checks are run

**Examples:**

```bash
# Run all security checks on default namespace
$ citrouille security

# Run security checks on production
$ citrouille security production

# Run only configuration checks
$ citrouille security production --check-config

# Run only network checks
$ citrouille security production --check-network

# Get JSON output
$ citrouille -o json security production
```

**Sample Output:**

```bash
================================================================================
SECURITY AUDIT
================================================================================

Total findings: 15
  CRITICAL: 2, HIGH: 5, MEDIUM: 6, LOW: 2

--------------------------------------------------------------------------------

[CRITICAL] 2 finding(s)

  [1] Privileged Container (CWE-250)
      Resource: Deployment - payment-service
      Container: payment-app
      Issue: Container is running in privileged mode
      Details: Privileged containers have access to all host devices

  [2] Host Network Enabled (CWE-250)
      Resource: Deployment - debug-pod
      Container: N/A
      Issue: Pod is using host network namespace
      Details: Pods with hostNetwork can bypass network policies
```

**Exit Codes:**
- `0` - No critical or high severity findings
- `1` - Critical or high severity findings detected



## Configuration File

To simplify command usage, you can create a configuration file at `~/.config/citrouille/config.yaml`.

Set a default kubeconfig file path to avoid typing `--kubeconfig` every time, and create friendly names for complex namespace names.

```yaml
kubeconfig: /home/user/.kube/production-cluster-config
namespaces:
  prod: microservices-production-us-east-1
  int: microservices-integration-us-east-1
  dev: microservices-development-us-east-1
```



## Reporting Issues

Visit the following link to report an issue. [Github Issues](https://github.com/Chelsea486MHz/citrouille/issues)