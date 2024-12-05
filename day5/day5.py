from math import floor

class UpdateValidator:
    def __init__(self, fileName):
        with open(fileName, 'r') as data:
            self.source = data.read()
            rawRules, rawUpdates = self.source.split('\n\n')
            processedRules = list(map(
                lambda r: r.split('|'), rawRules.split('\n')
            ))
            processedRules = list(map(
                lambda r: list(map(
                    lambda val: int(val),
                    r)),
                processedRules))
            self.rules = processedRules

            processedUpdates = list(map(
                    lambda u: u.split(','),
                    rawUpdates.split('\n')
                ))
            processedUpdates = list(filter(lambda u: u != [''], processedUpdates))
            processedUpdates = list(map(
                lambda u: list(map(
                    lambda val: int(val), 
                    u)), 
                processedUpdates)) 
            self.updates = processedUpdates

    def updateIsValid(self, update):
        for i, val in enumerate(update):
            if i == len(update) - 1:
                return True
            for next_val in update[i+1:]:
                if [val, next_val] not in self.rules:
                    return False

    def getMidOfUpdate(self, update):
        return update[floor(len(update)/2)]

    # only corrects 1 error max
    def fixInvalidUpdate(self, update):
        update_copy = update.copy()
        while not self.updateIsValid(update_copy):
            for i in range(len(update_copy) - 1):
                for j in range(i + 1, len(update_copy)):
                    if [update_copy[i], update_copy[j]] not in self.rules:
                        # Swap the values
                        update_copy[i], update_copy[j] = update_copy[j], update_copy[i]
                        break
                else:
                    continue
                break
        return update_copy

    def sumValidUpdates(self):
        sum = 0
        for update in self.updates:
            if self.updateIsValid(update):
                sum += self.getMidOfUpdate(update)

        return sum

    def sumInvalidUpdates(self):
        sum = 0
        for update in self.updates:
            if not self.updateIsValid(update):
                # print(self.fixInvalidUpdate(update))
                sum += self.getMidOfUpdate(self.fixInvalidUpdate(update))

        return sum

uv = UpdateValidator("input.txt")
# print(uv.sumValidUpdates())
print(uv.sumInvalidUpdates())

