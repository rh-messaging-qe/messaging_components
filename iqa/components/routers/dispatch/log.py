# Getting log from current service ran
# journalctl -u qdrouterd --since "$(echo $(systemctl show -p ActiveEnterTimestamp qdrouterd) | awk '{print $2 $3}')" --no-pager
#
#


class Log:
    pass