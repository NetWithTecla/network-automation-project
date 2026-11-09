import os
import sys
import yaml
from jinja2 import Template
from datetime import datetime
from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException,NetmikoAuthenticationException

# =====================================================================
# FEATURE 1: ROBUST LOGGING & DIRECTORY STRUCTURE INITIALIZATION
# =====================================================================
# Automatically establish an isolated filesystem directory to anchor pre-change backups
BACKUP_DIR = "automated_backups"
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)
    print(f"[INIT] Established secure backup storage repository: '{BACKUP_DIR}/'")

# Generate an accurate, immutable down-to-the-minute timestamp index
current_timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# Load central asset properties from your inventory map database
print("[INIT] Parsing target device variables from inventory matrix 'data.yaml'...")
try:
    with open("data.yaml", "r") as file:
        inventory = yaml.safe_load(file)
except FileNotFoundError:
    print("[FATAL ERROR] Inventory target file 'data.yaml' does not exist. Halting execution pipeline.")
    sys.exit()

# Load the dynamic configuration layout code blueprint
print("[INIT] Compiling raw Jinja2 configuration design template code from 'template.j2'...")
try:
    with open("template.j2", "r") as file:
        template_raw_code = file.read()
except FileNotFoundError:
    print("[FATAL ERROR] Design template layout file 'template.j2' does not exist. Halting execution pipeline.")
    sys.exit()

jinja_blueprint_processor = Template(template_raw_code)

# =====================================================================
# SYSTEM CORE: ORCHESTRATION LAYER LOOP SEQUENCE
# =====================================================================
print(f"[START] Triggering infrastructure automation workflow pipeline for {len(inventory['routers'])} endpoints.")

for router_profile in inventory["routers"]:
    device_name = router_profile["name"]
    device_host = router_profile["host"]

    print("\n" + "="*70)
    print(f"[PROCESSING] Commencing operations for target node asset: {device_name} ({device_host})")

    # Strip custom naming flags to isolate vanilla credential parameters for Netmiko
    ssh_login_credentials = {key: value for key, value in router_profile.items() if key != 'name'}

    # =====================================================================
    # FEATURE 2: EXCEPTION HANDLING AND SESSION SANITIZATION
    # =====================================================================
    try:
        # Establish secure SSH transport tunnel across the switch infrastructure fabric
        print(f"   [SSH] Requesting secure session tunnel connection to port 22...")
        with ConnectHandler(**ssh_login_credentials) as net_connect:
            print(f"   [SSH] Authentication parameters verified successfully. Shell link is LIVE.")

            # Enter privilege exec mode immediately to guarantee access authority
            net_connect.enable()

            # =====================================================================
            # FEATURE 3: AUTOMATED ROLLS-BACK FALLBACK PRE-CHANGE BACKUPS
            # =====================================================================
            print(f"   [BACKUP] Extracting complete live running-config text profile from hardware memory...")
            live_running_config_data = net_connect.send_command("show running-config")

            # Construct a unique, traceable backup tracking file name index
            backup_filename_index = f"{BACKUP_DIR}/{device_name}_pre_change_{current_timestamp}.bak"

            with open(backup_filename_index, "w") as backup_file:
                backup_file.write(live_running_config_data)
            print(f"   [BACKUP] Fallback rollback snapshot written successfully to disk: '{backup_filename_index}'")

            # =====================================================================
            # FEATURE 4: DYNAMIC INTENT-BASED JINJA2 VARIABLES
            # =====================================================================
            print(f"   [JINJA2] Computing dynamic logical attributes and calculating local parameters...")
            # Automatically perform octet subnet arithmetic extraction mapping values on the fly
            host_identifier_octet = device_host.split(".")[-1]
            calculated_loopback_ip = f"{host_identifier_octet}.{host_identifier_octet}.{host_identifier_octet}.{host_identifier_octet}"

            # Compile variables right inside the layout placeholder tags
            compiled_configuration_commands = jinja_blueprint_processor.render(
                router_name=device_name,
                loopback_ip=calculated_loopback_ip
            )

            # =====================================================================
            # SYSTEM DELIVERY: SECURE DISPATCH LAYER
            # =====================================================================
            print(f"   [DEPLOY] Dispatching compiled configuration commands down the wire line...")
            deployment_logs = net_connect.send_config_set(compiled_configuration_commands.splitlines())
            print(f"   [DEPLOY] Configuration delta block passed to device successfully.")

            # =====================================================================
            # FEATURE 5: INTERACTIVE CONFIGURATION VERIFICATION (POST-CHECKS)
            # =====================================================================
            print(f"   [AUDIT] Launching interactive verification post-checks across interface metrics...")

            # Target the physical port configured inside your template context to read metrics
            verification_state_data = net_connect.send_command("show ip interface brief | include FastEthernet0/1")

            print(f"\n   [METRICS OUTPUT] --- Verification Diagnostics Report for {device_name} ---")
            print(f"   {verification_state_data.strip()}")
            print(f"   ------------------------------------------------------------------------")

    # EXCEPTION BLOCK ANCHORS: Isolates errors to prevent global program crashes
    except NetmikoTimeoutException:
        print(f"   ❌ [CONNECTION TIMEOUT ERROR] Router '{device_name}' at {device_host} is completely unreachable.")
        print(f"      [DIAGNOSTICS] Verify power status, check switch portfast states, and validate local adapter binding.")
    except NetmikoAuthenticationException:
        print(f"   ❌ [AUTHENTICATION DEFECT ERROR] SSH credentials rejected for router '{device_name}' at {device_host}.")
        print(f"      [DIAGNOSTICS] Check local username/password definitions in 'data.yaml' match Cisco AAA lines.")
    except Exception as general_system_fault:
        print(f"   ❌ [UNEXPECTED FAULT DETECTED] Script encountered an unhandled error condition: {general_system_fault}")
        print(f"      [DIAGNOSTICS] Check terminal interface syntax or template file layout parameters.")

print("\n" + "="*70)
print("[COMPLETED] Multi-endpoint infrastructure deployment automation pipeline run terminated cleanly.")
