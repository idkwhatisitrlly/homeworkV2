class InfoMessage:
    """�������������� ��������� � ����������."""
    
    message_template: str = ('��� ����������: {training_type}; '
                             '������������: {duration:.3f} �.; '
                             '���������: {distance:.3f} ��; '
                             '��. ��������: {speed:.3f} ��/�; '
                             '��������� ����: {calories:.3f}.')
    
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """������� ���������� � ����������."""
        return self.message_template.format(training_type=self.training_type,
                                            duration=self.duration,
                                            distance=self.distance,
                                            speed=self.speed,
                                            calories=self.calories)


class Training(ABC):
    """������� ����� ����������."""
    
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action_times = action
        self.duration_hour = duration
        self.weight_kg = weight

    @abstractmethod
    def get_spent_calories(self) -> float:
        """����������� ����� ��� ��������� ���������� ����������� �������."""
        pass

    def get_distance(self) -> float:
        """�������� ��������� � ��."""
        return self.action_times * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """�������� ������� �������� ��������."""
        return self.get_distance() / self.duration_hour

    def show_training_info(self) -> InfoMessage:
        """������� �������������� ��������� � ����������� ����������."""
        return InfoMessage(self.__class__.__name__,
                           self.duration_hour,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """����������: ���."""
    
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight_kg / self.M_IN_KM
                * (self.duration_hour * self.MINUTES_IN_HOUR))


class SportsWalking(Training):
    """����������: ���������� ������."""
    
    coe_ff1: float = 0.029
    coe_ff2: float = 0.035
    K: int = 2
    G: float = 0.278
    L: int = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)

        self.height_cm = height / self.L

    def get_spent_calories(self) -> float:
        """�������� ���������� ����������� ������� �� ����� ������."""
        SPEED_M = self.G * self.get_mean_speed()

        return ((self.coe_ff2 * self.weight_kg
                + (SPEED_M ** self.K / self.height_cm)
                * self.coe_ff1 * self.weight_kg)
                * (self.duration_hour * self.MINUTES_IN_HOUR))


class Swimming(Training):
    """����������: ��������."""
    
    LEN_STEP: float = 1.38
    COEFF_CALOR1: float = 1.1
    COEFF_CALOR2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_meters = length_pool
        self.count_pool_times = count_pool

    def get_mean_speed(self) -> float:
        """�������� ������� �������� �������� �� ����� ��������."""
        return (self.length_pool_meters * self.count_pool_times
                / self.M_IN_KM / self.duration_hour)

    def get_spent_calories(self) -> float:
        """�������� ���������� ����������� ������� �� ����� ��������."""
        return ((self.get_mean_speed() + self.COEFF_CALOR1) * self.COEFF_CALOR2
                * self.weight_kg * self.duration_hour)


def read_package(workout_type: str, data: list) -> Training:
    """��������� ������ ���������� �� ��������."""
    training_data: dict[str, type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in training_data:
        raise ValueError('������� �������� ������������� ����������.')
    return training_data[workout_type](*data)


def main(training: Training) -> None:
    """������� �������."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
