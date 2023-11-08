<img align="right" width="100" height="74" src="https://user-images.githubusercontent.com/8277210/183290025-d7b24277-dfb4-4ce1-bece-7fe0ecd5efd4.svg" />

# Port Message Sender GitHub Action

[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://join.slack.com/t/devex-community/shared_invite/zt-1bmf5621e-GGfuJdMPK2D8UN58qL4E_g)

Port is the Developer Platform meant to supercharge your DevOps and Developers, and allow you to regain control of your environment.


## Send Scorecard Report

Action to send a scorecard report to a Slack channel about the current state and progress in a scorecard.

### example

 ![Scorecard Report](docs/assets/scorecard-report.png)

### Usage

| Input                | Description                                                                                              | Required | Default |
|----------------------|----------------------------------------------------------------------------------------------------------|----------|---------|
| `port_client_id`     | Port Client ID                                                                                           | true     |         |
| `port_client_secret` | Port Client Secret                                                                                       | true     |         |
| `port_region`        | Port Region to use, if not provided will use the default region of the Port                        | false    | eu        |
| `slack_webhook_url`  | Slack Webhook URL                                                                                        | true     |         |
| `blueprint`          | Blueprint identifier                                                                                     | true     |         |
| `scorecard`          | Scorecard identifier                                                                                     | true     |         |
| `message_kind`       | Message kind to send, to send Scorecard Report, pass - `scorecard_report`                                | true     |         |
| `filter_rule`        | The [rule filter](https://docs.getport.io/search-and-query/#rules) to apply on the data queried from Port | false    |         |

```yaml
- uses: port-labs/port-sender@v0.1.11
  with:
    port_client_id: ${{ secrets.PORT_CLIENT_ID }}
    port_client_secret: ${{ secrets.PORT_CLIENT_SECRET }}
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
    blueprint: app
    scorecard: productionReadiness
    message_kind: scorecard_report
```

## Send Scorecard Reminder

A call to action to remind the team that some of their services didn't reach Gold level for specific scorecard.

### example

 ![Scorecard Reminder](docs/assets/scorecard-reminder.png)

### Usage

| Input                | Description                                                                   | Required | Default |
|----------------------|-------------------------------------------------------------------------------|----------|---------|
| `port_client_id`     | Port Client ID                                                                | true     |         |
| `port_client_secret` | Port Client Secret                                                            | true     |         |
| `port_region`        | Port Region to use, if not provided will use the default region of the Port | false    | eu        |
| `slack_webhook_url`  | Slack Webhook URL                                                             | true     |         |
| `blueprint`          | Blueprint identifier                                                          | true     |         |
| `scorecard`          | Scorecard identifier                                                          | true     |         |
| `message_kind`       | Message kind to send, to send Scorecard Reminder, pass - `scorecard_reminder` | true     |         |
| `filter_rule`        | The [rule filter](https://docs.getport.io/search-and-query/#rules) to apply on the data queried from Port | false    |         |

In this example you can see how we filter for specific team and send a reminder to them.

```yaml
- uses: port-labs/port-sender@v0.1.11
  with:
    port_client_id: ${{ secrets.PORT_CLIENT_ID }}
    port_client_secret: ${{ secrets.PORT_CLIENT_SECRET }}
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
    blueprint: service
    scorecard: Ownership
    message_kind: scorecard_reminder
    filter_rule: '{"property": "$team","operator": "containsAny","value": ["Backend Team"]}'
```