from .base import Base


class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'altr'
        self.kind = 'file'

    def on_init(self, context):
        context['__current_bufname'] = self.vim.call('bufname', '%')
        context['__rule_table'] = self.vim.call('altr#_rule_table')
        context['__direction'] = 'back'
        context['__bufname'] = context['__current_bufname']
        context['is_async'] = True

    def gather_candidates(self, context):
        return self._async_gather_candidates(context)

    def _async_gather_candidates(self, context):
        bufname = self.vim.call('altr#_infer_the_missing_path',
                                context['__bufname'],
                                context['__direction'],
                                context['__rule_table'])
        if self.vim.call('type', bufname) != self.vim.eval('v:t_string'):
            if context['__direction'] == 'back':
                context['__direction'] = 'forward'
            elif context['__direction'] == 'forward':
                context['is_async'] = False
            return []
        elif bufname == context['__current_bufname']:
            context['is_async'] = False
            return []

        context['__bufname'] = bufname
        return [{'word': bufname, 'action__path': bufname}]
