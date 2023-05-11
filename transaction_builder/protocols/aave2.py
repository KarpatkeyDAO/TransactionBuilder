from dataclasses import dataclass
from transaction_builder.util.constants import ETHAddr
from transaction_builder.util.functions import to_data_input

Address = str

AvatarSafeAddress = object()

@dataclass
class LoadedMethod:
    name: str
    target_address: Address
    data: str
    args: list


class Method:
    def __init__(self, name: str, signature, fixed_arguments: dict, variable_arguments: list, target_address):
        self.name = name
        self.signature = signature
        self.fixed_arguments = fixed_arguments
        self.variable_arguments = variable_arguments
        self.target_address = target_address
        self.avatar = None
        if set(fixed_arguments.keys()) | set(variable_arguments) != set(self.arg_names):
            raise ValueError("Bad Method definition: arguments don't match signature")

    def with_args(self, avatar: Address | None = None, target_address: Address | None = None, **kwargs):
        if set(kwargs.keys()) != set(self.variable_arguments):
            raise ValueError(f"Wrong arguments '{kwargs.keys()}', expected {self.variable_arguments}")
        if self.target_address is None:
            self.target_address = target_address
        else:
            if target_address is not None and target_address != self.target_address:
                raise ValueError("Target address is fixed to a different address")
        if self.target_address is None:
            raise ValueError("Target address must be provided")

        arg_values = []
        for arg_name, arg_type in self.signature:
            if arg_name in self.fixed_arguments:
                value = self.fixed_arguments[arg_name]
                if value is AvatarSafeAddress:
                    if avatar is None:
                        raise ValueError("Avatar address must be provided")
                    value = avatar
            else:
                value = kwargs[arg_name]
            arg_values.append(value)

        data = to_data_input(self.name, self.arg_types, arg_values)

        return LoadedMethod(name=self.name, target_address=self.target_address, data=data, args=arg_values)

    @property
    def arg_types(self):
        return [arg_type for arg_name, arg_type in self.signature]

    @property
    def arg_names(self):
        return [arg_name for arg_name, arg_type in self.signature]


deposit = Method(
    name='deposit',
    signature=[("asset", "address"), ("amount", "uint256"), ("onBehalfOf", "address"), ("referralCode", "uint16")],
    fixed_arguments={"onBehalfOf": AvatarSafeAddress, "referralCode": 0},
    variable_arguments=['asset', 'amount'],
    target_address=ETHAddr.AaveLendingPoolV2,
)

approve_for_aave_lending_poolv2 = Method(
    name='approve',
    signature=[("spender", "address"), ("amount", "uint256")],
    fixed_arguments={"spender": ETHAddr.AaveLendingPoolV2},
    variable_arguments=['amount'],
    target_address=None  # Token address
)
