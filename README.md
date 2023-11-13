<img align="right" width="100" height="74" src="https://user-images.githubusercontent.com/8277210/183290025-d7b24277-dfb4-4ce1-bece-7fe0ecd5efd4.svg" />

# Port Message Sender GitHub Action

[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://join.slack.com/t/devex-community/shared_invite/zt-1bmf5621e-GGfuJdMPK2D8UN58qL4E_g)

Port is an open internal developer portal. The portal contains valuable data about standards and compliance (in the form of scorecards or initiatives) about software catalog entities, such as the production readiness (scorecard) of a microservice (an entity).

This action will allow you to automatically send reports and reminders with regard to initiatives or scorecards, letting managers and developers know what standards need to be met that are relevant to them.

![Scorecard Report](docs/assets/scorecard-report.png)

## Pre-requisites

### Port

Find your Port credentials
To find your Port API credentials go to Port, hover on the 3 dots button at the top right corner, select Credentials and then you will be able to view and copy your `CLIENT_ID` and `CLIENT_SECRET`:

![Port Credentials](docs/assets/credentials-modal.png)

### Slack

Setting up a slack webhook
Head to your [Slack apps](https://api.slack.com/apps) page and create a new app (or select one of your existing apps). Then, go to the Incoming Webhooks page and create a new webhook, specifying the target channel on your server where messages that are sent to the slack webhook will be transferred.

Copy the webhook URL, you will use it soon to set up your GitHub action.

## Send Scorecard Report

Action to send a scorecard report to a Slack channel about the current state and progress in a scorecard.

### Output example

 ![Scorecard Report](docs/assets/scorecard-report.png)

### Usage

| Input                | Description                                                                                              | Required | Default |
|----------------------|----------------------------------------------------------------------------------------------------------|----------|---------|
| `port_client_id`     | Port Client ID                                                                                           | true     |         |
| `port_client_secret` | Port Client Secret                                                                                       | true     |         |
| `port_region`        | Port Region to use, if not provided will use the default region of Port                        | false    | eu        |
| `slack_webhook_url`  | Slack Webhook URL                                                                                        | true     |         |
| `blueprint`          | Blueprint identifier                                                                                     | true     |         |
| `scorecard`          | Scorecard identifier                                                                                     | true     |         |
| `message_kind`       | Message kind to send, to send Scorecard Report, pass - `scorecard_report`                                | true     |         |
| `filter_rule`        | The [rule filter](https://docs.getport.io/search-and-query/#rules) to apply on the data queried from Port | false    |         |

This action will send a scorecard report to a Slack channel about the current state and progress in a scorecard.

You can modify the schedule to run the report on a daily/weekly/monthly basis. For more information about scheduling, refer to the [GitHub Actions documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule).


```yaml
name: Scheduled Scorecards Report

on:
  schedule:
    ## run every day at 9am
    - cron: '0 9 * * *'
  workflow_dispatch:

jobs:
    generate-scorecard-report:
        runs-on: ubuntu-latest
        steps:
            - name: Generate Scorecard Report
              uses: port-labs/port-sender@v0.1.14
              with:
                message_kind: scorecard_report
                port_client_id: ${{ secrets.PORT_CLIENT_ID }}
                port_client_secret: ${{ secrets.PORT_CLIENT_SECRET }}
                slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
                blueprint: app
                scorecard: productionReadiness
```

## Send Scorecard Reminder

A call to action to remind the team that some of their services didn't reach Gold level for specific scorecard.

### Output example

 ![Scorecard Reminder](docs/assets/scorecard-reminder.png)

### Usage

| Input                | Description                                                                  | Required | Default |
|----------------------|------------------------------------------------------------------------------|----------|---------|
| `port_client_id`     | Port Client ID                                                               | true     |         |
| `port_client_secret` | Port Client Secret                                                           | true     |         |
| `port_region`        | Port Region to use, if not provided will use the default region of Port | false    | eu        |
| `slack_webhook_url`  | Slack Webhook URL                                                            | true     |         |
| `blueprint`          | Blueprint identifier                                                         | true     |         |
| `scorecard`          | Scorecard identifier                                                         | true     |         |
| `message_kind`       | Message kind to send, to send Scorecard Reminder, pass - `scorecard_reminder` | true     |         |
| `filter_rule`        | The [rule filter](https://docs.getport.io/search-and-query/#rules) to apply on the data queried from Port | false    |         |

This example will send a scheduled reminder to a Slack channel about all the services that didn't reach the Gold level in the `productionReadiness` scorecard for the Backend Team.

You can modify the schedule to run the reminder on a daily/weekly/monthly basis. For more information about scheduling, refer to the [GitHub Actions documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule).
You can also modify the filter rule to filter the services, ideally you would want to filter by team, so that each team will get a reminder about their services.

```yaml
name: Generate Scorecards Reminders

on:
  schedule:
    ## run every day at 9am
    - cron: '0 9 * * *'
  workflow_dispatch:

jobs:
    generate-scorecards-reminders:
        runs-on: ubuntu-latest
        steps:
            - name: Generate Scorecards Reminders
              uses: port-labs/port-sender@v0.1.14
              with:
                message_kind: scorecard_reminder
                port_client_id: ${{ secrets.PORT_CLIENT_ID }}
                port_client_secret: ${{ secrets.PORT_CLIENT_SECRET }}
                slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
                blueprint: app
                scorecard: productionReadiness
                filter_rule: '{"property": "$team","operator": "containsAny","value": ["Backend Team"]}'
```

You can find more examples in the [examples folder](docs/examples/)
