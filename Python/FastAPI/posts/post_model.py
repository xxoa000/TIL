from sqlalchemy import false


# server_default=false() : DB 기본값, 새 커럶 추가시 기존 데이터의 값도 채워지도록 적용함.
# false() : SQLAlchemy가 SQL의 거짓 값을 표현하도록 제공하는 함수. false 를 import 해서 사용한다.

post_is_notice: Mapped[bool] = mapped_column(
    nullable=False,
    default=False,
    server_default=false()
)
