import unittest
# from __init__ import combine_frame_stamps

# list_dicts = [{'1':10,},{'2':20}]
#
# combine_frame_stamps(list_dicts)

class TestSum(unittest.TestCase):

    # simple order of two dicts
    def test_correct_order_default(self):
        dict_primary   = {"1":10,"2":20,"3":30}
        dict_secondary = {"4":40,"5":50,"6":60}
        dict_list      = [dict_primary,dict_secondary]
        dict_expected  = {"1":10,"2":20,"3":30,"4":40,"5":50,"6":60}
        dict_result = combine_frame_stamps(dict_list)
        self.assertDictEqual(dict_result,dict_expected)

    def test_only_primary_has_QR(self):
        dict_primary   = {"1":10,"2":20,"3":30}
        dict_secondary = {}
        dict_list      = [dict_primary,dict_secondary]
        dict_expected  = dict_primary
        dict_result = combine_frame_stamps(dict_list)
        self.assertDictEqual(dict_result,dict_expected)

    # topics in secondary area bigger than in primary, but behind in time
    def test_secondary_behind_primary(self):
        dict_primary   = {"1":40,"2":50,"3":60}
        dict_secondary = {"4":10,"5":20,"6":30}
        dict_list      = [dict_primary,dict_secondary]
        dict_expected  = dict_secondary
        dict_result = combine_frame_stamps(dict_list)
        self.assertDictEqual(dict_result,dict_expected)

    def test_intersected_topics(self):
        dict_primary   = {"1":10,"2":20,"3":30,"4":40,"5":50,"6":60}
        dict_secondary = {"1":5 ,"2":25,"3":35,"4":36,"5":40,"6":70}
        dict_list      = [dict_primary,dict_secondary]
        dict_expected  = {"1":10,"2":25,"3":35,"4":40,"5":50,"6":70}
        dict_result = combine_frame_stamps(dict_list)
        self.assertDictEqual(dict_result,dict_expected)

    # topics in middle missing from primary and secondary
    def test_missing_topics(self):
        dict_primary   = {"1":10,"2":20}
        dict_secondary = {"5":40,"6":60}
        dict_list      = [dict_primary,dict_secondary]
        dict_expected  = {"1":10,"2":20,"5":40,"6":60}
        dict_result = combine_frame_stamps(dict_list)
        self.assertDictEqual(dict_result,dict_expected)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
