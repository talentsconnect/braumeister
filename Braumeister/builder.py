#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from braumeister.actions.candidate import Candidate
from braumeister.actions.release import Release
from braumeister.actions.finalize import Finalize
from braumeister.actions.cleanup import Cleanup
class Builder:

    def __init__(self, action, fix_version, resume, update_jira):
        self.action = action
        self.fix_version = fix_version
        self.resume = resume
        self.update_jira = update_jira

    def execute(self):
        action = None
        if ('candidate' == self.action):
            action = Candidate(self.fix_version, self.resume, self.update_jira)
        elif ('release' == self.action):
            action = Release(self.fix_version, self.resume, self.update_jira)
        elif ('finalize' == self.action):
            action = Finalize(self.fix_version, self.resume, self.update_jira)
        elif ('cleanup' == self.action):
            action = Cleanup(self.fix_version, self.resume, self.update_jira)

        action.execute()
