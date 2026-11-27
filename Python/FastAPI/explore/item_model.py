class ItemSource(Base):
    __tablename__ = "item_sources"

    # ...

    # Decimal: 소수점 자리까지 정확하게 쓰기 위한 타입. 0~1 사이의 숫자로 작성한다. 백분율 구할시엔 해당 값 x 100
    # Numeric(m,n): 소수점이 있는 숫자를 정확하게 쓰기 위한 DB 타입. 첫 인자는 총 자리 수, 둘째 인자는 소수점 아래 수를 뜻함.
    drop_rate: Mapped[Decimal | None] = mapped_column(
        Numeric(3, 2),
        comment="획득 확률: 0~1, 확률을 직접 적용하지 않으면 NULL"
    )
