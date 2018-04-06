import block
import player
import solver
import transaction

def test_calcPercentStake():
    player.Player.id = 0
    
    p = [player.Player(i) for i in range(10)]
    s = solver.Solver(p, 10)

    assert s.calcPercentStake() == [0, 1/45, 2/45, 3/45, 4/45,
                                    5/45, 6/45, 7/45, 8/45, 9/45]

def test_chooseValidators():
    player.Player.id = 0
    
    p = [player.Player(0), player.Player(1), player.Player(1), player.Player(2), player.Player(4), player.Player(8), player.Player(16)]
    count = [0]*len(p)
    s = solver.Solver(p, 10)

    nRounds = 10000

    for i in range(nRounds):
        validators = s.chooseValidators()
        validators = [j.id for j in validators]
        for j in validators:
            count[j] += 1

    expected = [nRounds*s.nValidators*i for i in s.calcPercentStake()]

    error = 0.1

    for i, j in zip(count[1:], expected[1:]):
        assert abs((i-j)/j) < error

    assert count[0] == 0

