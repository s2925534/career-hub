# Restore Notes

`scripts/backup-career-hub.sh` creates timestamped, additive backups under
`${CAREER_HUB_BASE_PATH}/backups/<timestamp>/`. There is deliberately no automatic
"restore" script, because restoring is destructive to current state and should be a
deliberate, reviewed action.

## To restore manually

1. Stop the running app first: `docker compose down`.
2. Pick the backup timestamp you want to restore from:
   `ls ${CAREER_HUB_BASE_PATH}/backups/`.
3. For each folder you need to restore (`database`, `uploads`, `templates`,
   `generated/resumes`, `public/cv`, `exports`, `audit`), copy it back over the live
   folder, e.g.:
   ```
   cp -R "${CAREER_HUB_BASE_PATH}/backups/<timestamp>/database" \
         "${CAREER_HUB_BASE_PATH}/database.restored"
   ```
   Review the restored copy before replacing the live folder (e.g. rename the current
   live folder aside first, rather than deleting it, until you've confirmed the restore
   is what you wanted).
4. Restart the app: `docker compose up -d`.
5. Run `scripts/health-check.sh` to confirm the app is healthy after restore.

## Notes

- Backups are plain file copies, not database dumps — for the SQLite MVP, copying the
  `database` folder while the app is stopped (so the file isn't being written to) is
  sufficient.
- Backups are not currently encrypted. If you copy backups off-box, ensure that
  destination is itself access-controlled.
- See `docs/security.md` for the broader backup/restore and account-recovery model.
