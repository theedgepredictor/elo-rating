# ELO Rating

## ETL for Generating Sport Elos from ESPN API

This service will:
1. Extract data from the ESPN API
2. Handle attribute selection from the sport event payloads 
3. Apply ELO calculations to each event
4. Store ELO for each sport and handle upsert logic as needed

## Resources 

- [ELO Rating](https://en.wikipedia.org/wiki/Elo_rating_system)
- [ESPN Api Hidden Docs](https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b)