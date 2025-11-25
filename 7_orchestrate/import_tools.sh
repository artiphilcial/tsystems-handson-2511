#!/bin/bash

for f in ./tools/*.py; do
  echo "Importing file $f"
  orchestrate tools import -f "$f" --kind flow
done

orchestrate agents import -f agents/orchestrating_agent/customer_service_orchestrator.yaml
