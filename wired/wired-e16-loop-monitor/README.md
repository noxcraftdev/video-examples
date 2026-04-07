# Loop Monitor

Use Claude Code's `/loop` command to poll deploy status automatically.

## Usage

```bash
# Reset the counter
rm -f /tmp/deploy_check_counter

# Start polling every 30 seconds
/loop 30s bash check_deploy.sh
```

## What happens

- Check 1: all services healthy
- Check 2: all services healthy
- Check 3+: auth-service fails -- Claude reports the error

## Persistent scheduling

For monitoring that survives the session, use `CronCreate`:

```
CronCreate: cron "*/5 * * * *", prompt "Run bash check_deploy.sh and report if any service is failing"
```
