class Report:
    def __init__(self, **kwargs):
        self.group_structure = kwargs['group_structure']
        self.task_list = kwargs['task_list']
        self.result = None

    def run(self):
        self.result = self.group_structure[0](task_list=self.task_list)
        self.result.parse()

        for item in self.result.group_list:
            item.group_list = self.__make_group(
                item.task_list, self.group_structure, 0)

    def __make_group(self, task_list, group_iterator, index):
        index = index + 1
        if index == len(group_iterator):
            return
        cl = group_iterator[index]

        child = cl(task_list=task_list)
        child.parse()

        for item in child.group_list:
            item.group_list = self.__make_group(
                item.task_list, group_iterator, index)

        return child.group_list

    def __str__(self):
        return self.output

    @property
    def output(self):
        result_list = []
        since = min(self.task_list, key=lambda t: t.start).start
        until = max(self.task_list, key=lambda t: t.end).end

        result_list.append(
            f'\n\n*** Report for the period from {since.strftime("%Y-%m-%d")} until {until.strftime("%Y-%m-%d")}****')

        for item in self.result.group_list:
            result_list.append(str(item))
            l = self.__make_output(item.group_list, ' ')
            if not l:
                continue
            result_list.extend(l)

        return '\n'.join(result_list)

    def __make_output(self, group_list, space_index):
        if not group_list:
            return
        rl = []
        for item in group_list:
            rl.append(f'{space_index}{str(item)}')
            l = self.__make_output(item.group_list, f'{space_index}   ')
            if not l:
                continue
            rl.extend(l)
        return rl
