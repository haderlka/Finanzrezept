import unittest
from .asset_allocation_questionnaire import *
from ..generic.constants import EXPECTED_REAL_RATE_OF_EQUITY_RETURN, EXPECTED_REAL_RATE_OF_BONDS_RETURN

class TestRiskNeedQuestionnaire(unittest.TestCase):
    def setUp(self):
        # Common test values
        pass
        
    def test_no_equity_needed(self):
        """Test case where target can be achieved with bonds alone"""
        current_value = "10000"
        target_value = "23000"  
        time_horizon = "10"  # 10 years
        monthly_savings = "100"  # 100 EUR per month
        expected_equity_return = 5
        expected_bond_return = 0
        equity_allocation = risk_need_questionnaire(
            current_value, 
            time_horizon, 
            monthly_savings, 
            target_value,
            expected_equity_return,
            expected_bond_return
        )
        risk_need = equity_allocation_to_risk_need(equity_allocation)
        print(equity_allocation, risk_need)
        #self.assertEqual(equity_allocation, 0.0)
        self.assertEqual(risk_need, "Niedrig")    


if __name__ == '__main__':
    unittest.main() 