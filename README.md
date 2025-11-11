![project logo](./docs/logo.png)

**Status (main branch)**

![Maintained](https://img.shields.io/badge/Maintained-yes-green)
![License](https://img.shields.io/badge/License-GPL-red)
![Status](https://img.shields.io/badge/Status-build-blue)

# Pin down the root cause.

With `citrouille`, a CLI utility to quickly check Kubernetes deployments, engineers using Kubernetes in their products can now check the status of their deployments, pods, and namespaces, without having to spend too much time learning Kubernetes.

**Inventory features:**
- Produce readable documentation of current deployments and their images
- Track deployments in time, their creation/update times
- JSON exports for toolchain integration

**Blue/green features:**
- Compare namespaces, identify differences
- Ensure a safe transition between your environments

**Security features:**
- **At the cluster level:** Check for NetworkPolicy or Ingress issues and misconfigurations
- **At the image level:** Generate software bills of materials (SBOMs) and identify enumerated vulnerabilities (CVEs) with Trivy integration
- **At the product level:** check versions, creation date

**Installation manual**

See [installation-manual.md](./installation-manual.md)

**User manual**

See [user-manual.md](./user-manual.md)

**Contributions**

See [CONTRIBUTING.md](./contributing.md)

**Code of conduct**

See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)

**Active contributors**

Chelsea Murgia <[mail@chelsea486mhz.fr](mailto:mail@chelsea486mhz.fr)>