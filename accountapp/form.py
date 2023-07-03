from django.contrib.auth.forms import UserCreationForm

class AccountUpdateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 회원 수정시 아이디를 변경 못하게 비활성화
        self.fields['username'].disabled = True
