from paperspace.commands import CommandBase


class _JobsCommandBase(CommandBase):
    def _log_message(self, response, success_msg_template, error_msg):
        if response.ok:
            try:
                handle = response.json()
            except (ValueError, KeyError):
                self.logger.log(success_msg_template)
            else:
                msg = success_msg_template.format(**handle)
                self.logger.log(msg)
        else:
            try:
                data = response.json()
                self.logger.log_error_response(data)
            except ValueError:
                self.logger.log(error_msg)


class DeleteJobCommand(_JobsCommandBase):
    def execute(self, job_id):
        url = "/jobs/{}/destroy/".format(job_id)
        response = self.api.post(url)
        self._log_message(response,
                          "Job deleted",
                          "Unknown error while deleting job")


class CreateJobCommand(_JobsCommandBase):
    def execute(self, **kwargs):
        url = "/jobs/create"
