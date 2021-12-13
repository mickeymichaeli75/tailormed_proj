class assistance_program:
    def __init__(self,name = None,eligible_treatments = [], is_open = None, is_re_enrollment = None, grant_amount = "$0"):
        self.name = name
        self.eligible_treatments = eligible_treatments
        self.is_open = is_open
        self.is_re_enrollment = is_re_enrollment
        self.grant_amount = grant_amount
        
    def __repr__(self):
        ans = self.name + ", "
        if self.is_re_enrollment:
            ans = ans + "Re-enrollment Only"
        elif self.is_open:
            ans = ans + "Open"
        else:
            ans = ans + "Closed"
        ans = ans + ", "
        ans = ans + self.grant_amount
        return ans
