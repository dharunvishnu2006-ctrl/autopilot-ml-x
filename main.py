from src.ingestor import AutoPilotIngestor

ingestor = AutoPilotIngestor(["data/sample_orders.csv"])
reports = ingestor.run()

for report in reports:
    print(report)
