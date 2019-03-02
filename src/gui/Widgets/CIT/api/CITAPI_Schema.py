from marshmallow import Schema, fields


class VMSuspendSchema(Schema):
    vmName = fields.String(required=True)


class VMStartSchema(Schema):
    vmName = fields.String(required=True)


class VMStatusSchema(Schema):
    vmName = fields.String(required=True)
    mgrStatus = fields.String()


class VMConfigSchema(Schema):
    vmName = fields.String()
    adpt_number = fields.String()
    src_ip = fields.String()
    dst_ip = fields.String()
    src_prt = fields.String()
    dst_prt = fields.String()


class LoginSchema(Schema):
    ip = fields.String(required=True)


class PlatformSchema(Schema):
    platform_name = fields.String(required=True)
    username = fields.String(required=True)
    group_identifier = fields.Int(required=True)
    task_type = fields.String(required=True)


login_schema = LoginSchema()
vm_config_schema = VMConfigSchema()
vm_status_schema = VMStatusSchema()
vm_start_schema = VMStartSchema()
vm_suspend_schema = VMSuspendSchema()
platform_schema = PlatformSchema()
