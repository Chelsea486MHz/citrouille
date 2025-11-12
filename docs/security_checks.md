# Security checks

Citrouille can perform basic security checks on containers.

## 1. Privileged containers

**CWE-250**: Execution with Unnecessary Privileges

### Indicators:
- `spec.template.spec.containers[].securityContext.privileged` (Should be `false`)
- `spec.template.spec.initContainers[].securityContext.privileged` (Should be `false`)

### Reasoning:
- Prevents the container from accessing dangerous host features like kernel modules or `/dev/`



## 2. Host PID namespace sharing

**CWE-653**: Improper Isolation or Compartmentalization

### Indicators:
- `spec.template.spec.hostPID` (Should be `false`)

### Reasoning:
- Prevents the container from sharing the host's process namespace



## 3. Host IPC usage

**CWE-653**: Improper Isolation or Compartmentalization

### Indicators:
- `spec.template.spec.hostIPC` (Should be `false`)

### Reasoning:
- Prevents the container from accessing the host's System V IPC objects (shared memory, semaphores, message queues)



## 4. Host network access

**CWE-653**: Improper Isolation or Compartmentalization

### Indicators:
- `spec.template.spec.hostNetwork` (Should be `false`)

### Reasoning:
- Prevents the container from sniffing traffic on the host or binding to its ports



## 5. Running as `root`

**CWE-250**: Execution with Unnecessary Privileges

### Indicators:
- `spec.template.spec.containers[].securityContext.runAsNonRoot` (Should be `true`)
- `spec.template.spec.containers[].securityContext.runAsUser` (Should not be `0`)
- `spec.template.spec.initContainers[].securityContext.runAsNonRoot` (Should be `true`)
- `spec.template.spec.initContainers[].securityContext.runAsUser` (Should not be `0`)
- `spec.template.spec.securityContext.runAsNonRoot` (Should be `true`)
- `spec.template.spec.securityContext.runAsUser` (Should not be `0`)

### Reasoning:
- Prevents the container from running as `root`
- Enforces the creation a dedicated user in the Dockerfile.



## 6. `allowPrivilegeEscalation` set to `true`

**CWE-269**: Improper Privilege Management

### Indicators:
- `spec.template.spec.containers[].securityContext.allowPrivilegeEscalation` (Should be `false`)
- `spec.template.spec.initContainers[].securityContext.allowPrivilegeEscalation` (Should be `false`)

### Reasoning:
- Prevents the use of `setUID` binaries.



## 7. Dangerous capabilities

**CWE-250**: Execution with Unnecessary Privileges

### Indicators:
- `spec.template.spec.containers[].securityContext.capabilities.add[]` (Should not be used)
- `spec.template.spec.containers[].securityContext.capabilities.drop[]` (Should be `ALL`)
- `spec.template.spec.initContainers[].securityContext.capabilities.add[]` (Should not be used)
- `spec.template.spec.initContainers[].securityContext.capabilities.drop[]` (Should be `ALL`)

### Reasoning:
- Prevents containers from using capabilities they shouldn't

### Notes:
Some dangerous capabilities:
- **SYS_ADMIN**: Mount filesystems, load kernel modules
- **NET_ADMIN**: Manipulate network interfaces/firewall, bypass NetworkPolicies, sniff traffic
- **SYS_PTRACE**: Trace/debug processes, read process memory, inject code into other processes
- **SYS_MODULE**: Load kernel modules
- **SYS_RAWIO**: Direct hardware access
- **DAC_READ_SEARCH**: Bypass file read permissions
- **DAC_OVERRIDE**: Bypass file permissions entirely
- **CHOWN**: Change file ownership
- **SETUID/SETGID**: Change process UID/GID



## 8. No resource limits

**CWE-770**: Allocation of Resources Without Limits or Throttling

### Indicators:
- `spec.template.spec.containers[].resources.limits.memory` (Should be set to the maximum memory the container needs)
- `spec.template.spec.containers[].resources.limits.cpu` (Should be set to the maximum CPU usage the container needs)
- `spec.template.spec.containers[].resources.requests.memory` (Should be set to the minimum memory the container needs)
- `spec.template.spec.containers[].resources.requests.cpu` (Should be set to the minimum CPU usage the container needs)
- `spec.template.spec.initContainers[].resources.limits.memory` (Should be set to the maximum memory the container needs)
- `spec.template.spec.initContainers[].resources.limits.cpu` (Should be set to the maximum CPU usage the container needs)
- `spec.template.spec.initContainers[].resources.requests.memory` (Should be set to the minimum memory the container needs)
- `spec.template.spec.initContainers[].resources.requests.cpu` (Should be set to the minimum CPU usage the container needs)

### Reasoning:
- Not setting those allows attackers to perform denial of service attacks from compromised containers



## 9. `hostPath` usage

**CWE-668**: Exposure of Resource to Wrong Sphere

### Indicators:
- `spec.template.spec.volumes[].hostPath` (Should not be used)

### Reasoning:
- Mounting host files contradicts container isolation principles



## 10. Writable root filesystem

**CWE-732**: Incorrect Permission Assignment for Critical Resource

### Indicators:
- `spec.template.spec.containers[].securityContext.readOnlyRootFilesystem` (Should be set to `true`)
- `spec.template.spec.initContainers[].securityContext.readOnlyRootFilesystem` (Should be set to `true`)

### Reasoning:
- Prevents persistence, malware loading, general tampering in case of container compromission

### Notes:
- Most pods won't like this. As a compromise, we allow writable `tmpfs` instances on `/tmp` and `/var/tmp`
- See [ANSSI-BP-028-R28](https://cyber.gouv.fr/sites/default/files/document/linux_configuration-en-v2.pdf) (page 33)



## 11. Unspecified `seccomp` profile

**CWE-250**: Execution with Unnecessary Privileges

### Indicators:
- `spec.template.spec.securityContext.seccompProfile` (Should be `RuntimeDefault`)
- `spec.template.spec.containers[].securityContext.seccompProfile` (Should be `RuntimeDefault`)
- `spec.template.spec.initContainers[].securityContext.seccompProfile` (Should be `RuntimeDefault`)

### Reasoning:
- Prevents compromised containers from exploiting most syscall-based escape vulnerabilities



## 12. Automounted account tokens

**CWE-522**: Insufficiently Protected Credentials

### Indicators:
- `spec.template.spec.automountServiceAccountToken` (Should be `false`)
- `spec.serviceAccountName` (Should be unique to the pod)

### Reasoning:
- Prevents compromised containers from gaining access to the Kubernetes cluster



## 13. Mutable image tags

**CWE-494**: Download of Code Without Integrity Check

### Indicators:
- `spec.template.spec.containers[].image`
- `spec.template.spec.initContainers[].image`

### Reasoning:
- Compromised registries could lead to stealthy compromission of containers through mutable image replacement

### Notes:
Container images can be referenced by:
- **latest**: `nginx:latest` (always changes)
- **tag**: `nginx:1.21` (can be overwritten)
- **digest**: `nginx@sha256:abc123...` (immutable)



## 14. Hardcoded secrets in environment variables

**CWE-798**: Use of Hard-coded Credentials

### Indicators:
- `spec.template.spec.containers[].env[].value`
- `spec.template.spec.initContainers[].env[].value`

### Reasoning:
- Prevents secret disclosure in compromised containers/etcd/backups/kubectl workstations

### Notes:
- `kubectl` can show environment variables in plain text
- The deployment YAML stored in etcd and backups contain the secrets in plain text



## 15. Namespace enforcement of PSS

**CWE-693**: Protection Mechanism Failure

### Indicators:
- `metadata.labels.pod-security.kubernetes.io/enforce` (Should be `restricted` or `baseline`)
- `metadata.labels.pod-security.kubernetes.io/warn` (Should be set to provide warnings)
- `metadata.labels.pod-security.kubernetes.io/audit` (Should be set for audit logging)

### Reasoning:
- Prevents containers within the namespace from drifting from the PodSecurity standard



## 16. Check for mutable `configMap`/`secret` instances

**CWE-471**: Modification of Assumed-Immutable Data (MAID)

### Indicators:
- `configMap.immutable` (Should be `true`)
- `secret.immutable` (Should be `true`)

### Reasoning:
- Prevents runtime tampering for some configuration/secrets



## 17. Check for unset `emptyDir` size limits

**CWE-770**: Allocation of Resources Without Limits or Throttling

### Indicators:
- `spec.template.spec.volumes[].emptyDir.sizeLimit` (Should be set to a reasonable limit)

### Reasoning:
- Prevents denial of service attacks



## 18. Unspecified `securityContext.procMount`

**CWE-200**: Exposure of Sensitive Information to an Unauthorized Actor

### Indicators:
- `spec.template.spec.containers[].securityContext.procMount` (Should not be `unmasked`)
- `spec.template.spec.initContainers[].securityContext.procMount` (Should not be `unmasked`)

### Reasoning:
- Prevents compromised containers from accessing sensitive host information via `/proc`



## 19. Misconfigured `Role` or `ClusterRole`

**CWE-269**: Improper Privilege Management

### Indicators:
- `rules[].verbs[]` (Should not be `*`)
- `rules[].resources[]` (Should not be `*`)
- `rules[].apiGroups[]` (Should not be `*`)
- `rules[].verbs[]` containing `create` with `rules[].resources[]` containing `pods` (Should not be allowed together)
- `rules[].verbs[]` containing `create` or `patch` with `rules[].resources[]` containing `pods/exec` or `pods/attach` (Should not be allowed)
- `rules[].resources[]` containing `secrets` with `rules[].verbs[]` containing `get`, `list`, or `watch` (Should be scoped to specific secret names)
- `rules[].verbs[]` containing `impersonate` (Should not be granted)
- `rules[].verbs[]` containing `bind` or `escalate` with `rules[].resources[]` containing `roles` or `clusterroles` (Should not be allowed together)
- `rules[].verbs[]` containing `patch` or `update` with `rules[].resources[]` containing `nodes` or `nodes/status` (Should not be allowed together)
- `rules[].verbs[]` containing `create` or `update` with `rules[].resources[]` containing `persistentvolumes` (Should not be allowed together)
- `rules[].verbs[]` containing `create` or `update` with `rules[].resources[]` containing `podsecuritypolicies` (Should not be allowed together)
- `rules[].verbs[]` containing `create` with `rules[].resources[]` containing `serviceaccounts/token` (Should not be allowed together)

### Reasoning:
- Prevents privilege escalation by abusing RBAC misconfiguration

### Notes:
Particularly dangerous permission combinations:
- **pods/exec + pods/attach**: Execute commands in any pod
- **secrets (get/list)**: Read all secrets including service account tokens
- **create pods**: Create privileged pods with host access
- **impersonate**: Act as any user/group/service account
- **bind/escalate**: Assign roles with more permissions than you have



## 20. Misconfigured `RoleBinding` or `ClusterRoleBinding`

**CWE-269**: Improper Privilege Management

### Indicators:
- `roleRef.name` (Should not be `cluster-admin`)
- `subjects[].name` (Should not be `system:anonymous` or `system:unauthenticated`)

### Reasoning:
- Prevents privilege escalation by abusing RBAC misconfiguration

### Notes:
Particularly dangerous permission combinations:
- **pods/exec + pods/attach**: Execute commands in any pod
- **secrets (get/list)**: Read all secrets including service account tokens
- **create pods**: Create privileged pods with host access
- **impersonate**: Act as any user/group/service account
- **bind/escalate**: Assign roles with more permissions than you have



## 21. Shared process namespace

**CWE-653**: Improper Isolation or Compartmentalization

### Indicators:
- `spec.template.spec.shareProcessNamespace` (Should be `false`)

### Reasoning:
- Prevents containers from accessing each other's processes



## 22. Kernel tampering

**CWE-250**: Execution with Unnecessary Privileges

### Indicators:
- `spec.template.spec.securityContext.sysctls[].name` (Should not contain sysctls)

### Reasoning:
- Prevents compromised containers from attacking the kernel

### Notes:
Unsafe sysctls include:
- `kernel.*`: Kernel parameters that affect the entire node



## 23. Misconfigured `NetworkyPolicy`

**CWE-923**: Improper Restriction of Communication Channel to Intended Endpoints

### Indicators:
- `NetworkPolicy` (Should have at least 1 in namespace)

### Reasoning:
- Principle of least privilege
- Prevents exfils/lateral movement