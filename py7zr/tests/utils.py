from datetime import datetime
from py7zr.timestamp import UTC


def decode_all(archive):
    filenames = archive.getnames()
    for filename in filenames:
        cf = archive.getmember(filename)
        assert cf.filename == filename
        assert cf.lastwritetime is not None
        assert cf.checkcrc() is True, 'crc failed for %s' % (filename)
        assert len(cf.read()) == cf.uncompressed


def check_archive(archive):
    assert sorted(archive.getnames()) == ['test/test2.txt', 'test1.txt']
    assert archive.getmember('test2.txt') is None
    cf = archive.getmember('test1.txt')
    assert cf.checkcrc() is True
    assert cf.lastwritetime // 10000000 == 12786932628
    assert cf.lastwritetime.as_datetime().replace(microsecond=0) == \
        datetime(2006, 3, 15, 21, 43, 48, 0, UTC)
    assert cf.read() == bytes('This file is located in the root.', 'ascii')
    cf.reset()
    assert cf.read() == bytes('This file is located in the root.', 'ascii')
    cf = archive.getmember('test/test2.txt')
    assert cf.checkcrc() is True
    assert cf.lastwritetime // 10000000 == 12786932616
    assert cf.lastwritetime.as_datetime().replace(microsecond=0) == \
        datetime(2006, 3, 15, 21, 43, 36, 0, UTC)
    assert cf.read() == bytes('This file is located in a folder.', 'ascii')
    cf.reset()
    assert cf.read() == bytes('This file is located in a folder.', 'ascii')