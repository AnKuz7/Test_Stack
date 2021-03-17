import traceback


class TestRunner(object):
    def __init__(self, name):
        self.name = name
        self.testNo = 1

    def expectTrue(self, cond):
        try:
            if cond():
                self._pass()
            else:
                self._fail()
        except Exception as e:
            self._fail(e)

    def expectFalse(self, cond):
        self.expectTrue(lambda: not cond())

    def expectException(self, block):
        try:
            block()
            self._fail()
        except:
            self._pass()

    def _fail(self, e=None):
        print(f'FAILED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1
        if e is not None:
            traceback.print_tb(e.__traceback__)

    def _pass(self):
        print(f'PASSED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1


def match(string, pattern):
    if len(string) != len(pattern):
        return False 

    valid_pattern_character = set('ad* ')
    if not set(pattern).issubset(valid_pattern_character):
        raise ValueError('Thr pattern contains invalid characters')

    for index, string_character in enumerate(string):
        pattern_character = pattern[index]
        if string_character >= 'a' and string_character <= 'z':
            if pattern_character != 'a' and pattern_character != '*':
                return False
        elif string_character.isdigit():
            if pattern_character != 'd' and pattern_character != '*':
                return False
        elif string_character == ' ':
            if pattern_character != ' ':
                return False
        else:
            return False

    return True


def testMatch():
    runner = TestRunner('match')

    runner.expectFalse(lambda: match('xy', 'a'))
    runner.expectFalse(lambda: match('x', 'd'))
    runner.expectFalse(lambda: match('0', 'a'))
    runner.expectFalse(lambda: match('*', ' '))
    runner.expectFalse(lambda: match(' ',  'a'))

    runner.expectTrue(lambda:  match('01 xy', 'dd aa'))
    runner.expectTrue(lambda: match('1x', '**'))

    runner.expectException(lambda:  match('x', 'w'))



tasks = {
    'id': 0,
    'name': 'Все задачи',
    'children': [
        {
            'id': 1,
            'name': 'Разработка',
            'children': [
                {'id': 2, 'name': 'Планирование разработок', 'priority': 1},
                {'id': 3, 'name': 'Подготовка релиза', 'priority': 4},
                {'id': 4, 'name': 'Оптимизация', 'priority': 2},
            ],
        },
        {
            'id': 5,
            'name': 'Тестирование',
            'children': [
                {
                    'id': 6,
                    'name': 'Ручное тестирование',
                    'children': [
                        {'id': 7, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 8, 'name': 'Выполнение тестов', 'priority': 6},
                    ],
                },
                {
                    'id': 9,
                    'name': 'Автоматическое тестирование',
                    'children': [
                        {'id': 10, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 11, 'name': 'Написание тестов', 'priority': 3},
                    ],
                },
            ],
        },
        {'id': 12, 'name': 'Аналитика', 'children': []},
    ],
}


def findTaskHavingMaxPriorityInGroup(tasks, groupId):
    task_with_max_priority = None

    if tasks['id'] >= groupId:
        for tasks_child in tasks['children']:
            if 'children' not in tasks_child:
                if (task_with_max_priority is None or 
                    tasks_child['priority'] > task_with_max_priority['priority']):
                        task_with_max_priority = tasks_child
            else:
                task_with_max_priority_child = findTaskHavingMaxPriorityInGroup(tasks_child, groupId)
                if (task_with_max_priority is None or 
                        (task_with_max_priority_child is not None and
                        task_with_max_priority_child['priority'] > task_with_max_priority['priority'])):
                            task_with_max_priority = task_with_max_priority_child
                
    else:
        for index, tasks_child in enumerate(tasks['children']):
            if 'children' not in tasks_child:
                raise ValueError('Not a group')

            if index == len(tasks['children']) - 1:
                if tasks_child['id'] == groupId:
                    task_with_max_priority = findTaskHavingMaxPriorityInGroup(tasks_child, groupId)
                else:
                    raise ValueError('The group does not exist')
            elif groupId in range(tasks_child['id'], tasks['children'][index + 1]['id']):
                task_with_max_priority = findTaskHavingMaxPriorityInGroup(tasks_child, groupId)
                break

    return task_with_max_priority 


def taskEquals(a, b):
    return (
        not 'children' in a and
        not 'children' in b and
        a['id'] == b['id'] and
        a['name'] == b['name'] and
        a['priority'] == b['priority']
    )


def testFindTaskHavingMaxPriorityInGroup():
    runner = TestRunner('findTaskHavingMaxPriorityInGroup')

    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 13))
    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 2))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 12) is None)

    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 0), {
        'id': 8,
        'name': 'Выполнение тестов',
        'priority': 6,
    }))
    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 1), {
        'id': 3,
        'name': 'Подготовка релиза',
        'priority': 4,
    }))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 9)['priority'] == 3)

testMatch()
testFindTaskHavingMaxPriorityInGroup()