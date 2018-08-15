

class EditDis:

    @staticmethod
    def minDistance(ref, hyp):
        m, n = len(ref) + 1, len(hyp) + 1
        dp = [["" for i in range(n)] for j in range(m)]

        for i in range(n):
            dp[0][i] = i

        for i in range(m):
            dp[i][0] = i

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1]+1,
                               dp[i - 1][j - 1] + (0 if ref[i - 1] == hyp[j - 1] else 1),
                               )
        return dp[m - 1][n - 1] /  len(ref)


    @staticmethod
    def backtrace(bt, ref, hyp):
        res=[]
        op=[]
        ins, delt, sub = 0,0,0
        m, n = len(ref), len(hyp)
        while not (n==0 and m==0):
            if bt[m][n] == "C":
                res += ref[m-1]
                m -= 1; n -= 1
                op.append("C")
            elif bt[m][n] == "I":
                res.append("<ins>") #hyp[n-1][0]
                n -= 1
                ins+=1
                op.append("I")
            elif bt[m][n] == "I@":
                n -= 1
                op.append("I@")
            elif bt[m][n] == "D":
                res.append("<del>") # ref[m-1]
                m -= 1
                delt+=1
                op.append("D")
            elif bt[m][n] == "S":
                res.append(hyp[n-1][0])
                m -= 1; n -= 1
                sub+=1
                op.append("S")
            else:
                print("Error in bt:{:d} {:d} {} ref:{} hyp:{}, res:{} op:{}".format(m,n,bt[m][n], ref[m-1], hyp[n-1],res, op))                                                                                     
                break
        return reversed(res), (ins, delt, sub), " ".join(reversed(op))

    @staticmethod
    def m_minDistance(ref, hyp):
        m, n = len(ref)+1, len(hyp)+1
        dp = [[0 for i in range(n)] for j in range(m)]
        bt = [[0 for i in range(n)] for j in range(m)]

        cur_cost=0
        for i in range(n):
            if i != 0 and '@' not in hyp[i-1]:
                cur_cost = cur_cost + 1
                bt[0][i] = "I"
            else:
                bt[0][i] = "I@"
            dp[0][i] = cur_cost

        for i in range(m):
            dp[i][0] = i
            bt[i][0] = "D"

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = min(dp[i-1][j]+1, # Del
                               dp[i][j-1]+(0 if '@' in hyp[j-1] else 1), # Ins
                               dp[i-1][j-1] + (0 if ref[i-1] in hyp[j-1] else 1), #Sub
                               )

                if dp[i][j] == dp[i-1][j]+1:
                    # Del error
                    bt[i][j] = "D"
                elif dp[i][j] == dp[i][j-1] + (0 if '@' in hyp[j-1] else 1):
                    # Ins error
                    if '@' in hyp[j-1]:
                        bt[i][j] = "I@"
                    else:
                        bt[i][j] = "I"
                elif dp[i][j] == dp[i-1][j-1] + (0 if ref[i-1] in hyp[j-1] else 1):
                    if ref[i-1] in hyp[j-1]:
                        # correct
                        bt[i][j] = "C"
                    else:
                        # substitution error
                        bt[i][j] = "S"
                else:
                    print("ERROR editD error {} {} dp:{} min:{}".format(i,j, dp[i][j],min(dp[i-1][j]+(0 if '@' in hyp[j-1] else 1),
                               dp[i][j-1]+1,
                               dp[i-1][j-1] + (0 if ref[i-1] in hyp[j-1] else 1),
                               ) ))

        return dp[m-1][n-1] / len(ref), EditDis.backtrace(bt, ref, hyp), len(ref)
