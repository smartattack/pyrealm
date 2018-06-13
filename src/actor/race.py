"""
Player/NPC races
"""


class Race(object):
    """Race entity"""
    def __init__(self, name):
        self.name = name
        self.player_type = True
        self.description = None
        self._stats = {}
        self._max_stats = {}

    def load(self, name):
        """Attempt to load race from file"""
        if not name:
            log.error('Attempted to call Race.load without a name!')
            raise KeyError('Must include a name with load()')
        filename = os.path.join(GLOBALS.DATA_DIR, GLOBALS.RACE_DIR, name.lower() + '.json')
        data = ''
        log.info('+ Loading Race(%s)', name)
        with open(filename, "r") as file:
            for line in file:
                data += line
        try:
            loaded = from_json(data)
        except Exception as err:
            log.error('Could not load Race data: %s', err)
        if isinstance(loaded, Race):
            # Avoid resaving right away
            self._last_saved = time.time()
            self._checksum = hashlib.md5(data.encode('utf-8')).hexdigest()
            return loaded
        else:
            log.error('Loaded data != Race() - possible corruption')
            raise IOError('Failed to load race data from {}'.format(filename))


    def save(self, name):
        """Attempt to write race to file"""
        log.debug('FUNC: Race.save()')
        pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.RACE_DIR)
        try:
            os.makedirs(pathname, 0o755, True)
        except OSError as err:
            log.critical('Failed to create directory: %s -> %s', pathname, err)
        data = to_json(self, skip_list=['_checksum', '_last_saved'])
        checksum = make_checksum(data)
        if object_changed(self, checksum):
            self._checksum = checksum
            self._last_saved = time.time()
            log.info('+ Saving race: %s', self._name)
            filename = os.path.join(pathname, self._name.lower() + '.json')
            try:
                with open(filename, "w") as file:
                    file.write(data)
            except IOError as err:
                log.error('Saving race failed: %s', self.name.lower())                
