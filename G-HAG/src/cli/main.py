import argparse
try:
    import torch
except ImportError:
    torch = None
    nn = None
try:
    import numpy as np
except ImportError:
    np = None
from src.agents import NativelyRecursiveAgent, ResilientHAGModel, GeneralDataLoader
from src.desktop.agent import HAGDesktopAgent
from src.core.values import SystemValues

def main():
    values = SystemValues()
    parser = argparse.ArgumentParser(description=f"HAG {values.version} - Sovereign Intelligence Desktop Agent")
    parser.add_argument("--domain", type=str, default="physics", choices=["physics", "finance", "legal", "desktop"], help="Data domain to analyze")
    parser.add_argument("--query", type=str, default="Analyze current patterns", help="Query for the agent")
    parser.add_argument("--device", type=str, default="auto", help="Device to use (cuda/cpu/auto)")
    parser.add_argument("--desktop", action="store_true", help="Launch HAG-Desktop Executive Loop")

    args = parser.parse_args()

    if args.device == "auto":
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    else:
        device = torch.device(args.device)

    print(f"--- HAG {values.version} Initialized on {device} ---")

    if args.desktop or args.domain == "desktop":
        print("Launching Sovereign Desktop Agent...")
        agent = HAGDesktopAgent(agent_id="HAG-CLI-Desktop")
        result = agent.execute_desktop_task(args.query)

        print(f"\nTask: {result['task']}")
        print(f"Execution: {result['result']['status']} (LGA Secured)")
        print(f"E_desktop Score: {result['e_desktop']:.2f}")
        print(f"Perception Mode: {result['context']['perception_mode']}")
    else:
        loader = GeneralDataLoader(input_dim=16)
        x, y = loader.load_domain_data(domain=args.domain)

        if x is None:
            print(f"Error: Data for domain '{args.domain}' not found.")
            return

        model = ResilientHAGModel(input_dim=16)
        agent = NativelyRecursiveAgent(base_model=model)

        print(f"Processing query: '{args.query}' on {len(x)} samples...")
        result = agent.solve_complex_task(args.query, f"Domain: {args.domain}, Samples: {len(x)}")
        print(f"\nResult: {result}")

    print("\n--- HAG Sovereignty Protocol: Operation Complete ---")

if __name__ == "__main__":
    main()
