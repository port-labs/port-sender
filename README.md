<img align="right" width="100" height="74" src="https://user-images.githubusercontent.com/8277210/183290025-d7b24277-dfb4-4ce1-bece-7fe0ecd5efd4.svg" />

# Port Message Sender GitHub Action

[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://join.slack.com/t/devex-community/shared_invite/zt-1bmf5621e-GGfuJdMPK2D8UN58qL4E_g)

Port is the Developer Platform meant to supercharge your DevOps and Developers, and allow you to regain control of your environment.

### Docs

- [Port Docs](https://docs.getport.io/build-your-software-catalog/sync-data-to-catalog/ci-cd/github-workflow/)

## Usage

See [action.yml](action.yml) for inputs and outputs.


 ![Generate Scorecard Report](docs/assets/generate-scorecard-report.png)

```yaml
- uses: port-labs/port-sender@v0.1.19
  with:
    port_client_id: ${{ secrets.PORT_CLIENT_ID }}
    port_client_secret: ${{ secrets.PORT_CLIENT_SECRET }}
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
    blueprint: service
    scorecard: Ownership
    message_kind: scorecard_report
    filter_rule: '{"property": "$team","operator": "containsAny","value": ["Backend"]}'
```