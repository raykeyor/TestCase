class Stu:

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self,value):
        if not isinstance(value,int):
            raise ValueError("The value is not ")

        if value<0 and value>100:
            raise ValueError("The value shoud be between in (0,100)")

        self._score=value

stu=Stu()
stu.score=100