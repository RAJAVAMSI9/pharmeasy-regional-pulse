from metrics_engine import sales_dict, apr_may, may_jun, flagged_apr_may, flagged_may_jun

#TASK 3.1 CII INSIGHT GENERATOR
flagged_all = set(flagged_apr_may) | set(flagged_may_jun)

print(flagged_all)
print(len(flagged_all))

for region in sorted(flagged_all):
    if region in flagged_apr_may:
        apr = sales_dict[region].get('2026-04', 0)
        may = sales_dict[region].get('2026-05', 0)
        print(f"Region: {region} (April->May)")
        print(f"Context: In April 2026, {region} had sales of Rs {apr:.2f}.")
        print(f"Insight: By May 2026, sales changed to Rs {may:.2f}, a Month-on-Month change of {apr_may[region]:+.2f}%.")
        print(f"Implication: This change is large enough to warrant a human review before acting on it.")
        print()

    if region in flagged_may_jun:
        may = sales_dict[region].get('2026-05', 0)
        jun = sales_dict[region].get('2026-06', 0)
        print(f"Region: {region} (May->June)")
        print(f"Context: In May 2026, {region} had sales of Rs {may:.2f}.")
        print(f"Insight: By June 2026, sales changed to Rs {jun:.2f}, a Month-on-Month change of {may_jun[region]:+.2f}%.")
        print(f"Implication: This change is large enough to warrant a human review before acting on it.")
        print()

def draft_report_v1(flagged_regions, metrics):
    report = {}

    for region in flagged_regions["apr_may"]:
        apr = metrics["sales_dict"][region].get('2026-04', 0)
        may = metrics["sales_dict"][region].get('2026-05', 0)
        block = {
            "context": f"In April 2026, {region} had sales of Rs {apr:.2f}.",
            "insight": f"By May 2026, sales changed to Rs {may:.2f}, a Month-on-Month change of {metrics['apr_may'][region]:+.2f}%.",
            "implication": "This change is large enough to warrant a human review before acting on it."
        }
        report.setdefault(region, []).append(block)

    for region in flagged_regions["may_jun"]:
        may = metrics["sales_dict"][region].get('2026-05', 0)
        jun = metrics["sales_dict"][region].get('2026-06', 0)
        block = {
            "context": f"In May 2026, {region} had sales of Rs {may:.2f}.",
            "insight": f"By June 2026, sales changed to Rs {jun:.2f}, a Month-on-Month change of {metrics['may_jun'][region]:+.2f}%.",
            "implication": "This change is large enough to warrant a human review before acting on it."
        }
        report.setdefault(region, []).append(block)

    return report

metrics = {"sales_dict": sales_dict, "apr_may": apr_may, "may_jun": may_jun}
flagged_regions = {"apr_may": flagged_apr_may, "may_jun": flagged_may_jun}

report = draft_report_v1(flagged_regions, metrics)
print(len(report))
print(report["Guntur"])
