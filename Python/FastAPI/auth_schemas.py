# BaseModel: 요청, 응답 데이터 구조오 검증 규칙 정의
class UserCreate(BaseModel):
    """ 회원가입 요청 데이터와 입력값 검증 규칙. """

    # EmailStr: pydantic 이 이메일 형식 검증 및 정규화 할때 사용한다.
    email: EmailStr
    name: str = Field(
        min_length=4,
        max_length=50,
        pattern=r"^[가-힣A-Za-z0-9_]+$",
    )
    # SecretStr : 비밀번호 입력시 **** 로 보이도록 변환한다. 검증은 따로 필요하다.
    password: SecretStr = Field(
        min_length=8,
        max_length=128
    )

    # @field_validator() 를 붙이면 해당 클래스를 만들때 자동으로 호출된다.
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: SecretStr) -> SecretStr:
        if not re.fullmatch(r"[a-z0-9_]+", value.get_secret_value()):
            raise ValueError("비밀번호는 영문 소문자, 숫자, _만 사용할 수 있습니다.")
        return value
