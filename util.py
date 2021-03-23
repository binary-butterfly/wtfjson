# encoding: utf-8

"""
binary butterfly common
Copyright (c) 2017 - 2021, binary butterfly GmbH
All rights reserved.
"""


class UnsetValue:
    def __str__(self):
        return '<unset value>'

    def __repr__(self):
        return '<unset value>'

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False

    def __iter__(self):
        yield

    def __len__(self):
        return 0

    def __getitem__(self, index):
        return None


unset_value = UnsetValue()
