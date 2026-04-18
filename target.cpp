
// https://codeforces.com/contest/1824/problem/C
#include <bits/stdc++.h>
#define ll long long
#define vi vector<int>
#define pb push_back
using namespace std;

const int N = 2e5+5;
int n;
int a[N];
vi g[N];
set<int> st[N];
int dp[N];

void dfs(int u, int p, int c_xor) {
    c_xor ^= a[u];
    vi ch;
    
    for(int v : g[u]) {
        if(v == p) continue;
        ch.pb(v);
        dfs(v, u, c_xor);
    }

    if(ch.empty()) {
        st[u].insert(c_xor);
        dp[u] = 0;
        return;
    }

    //Removed small-to-large 'mxi' finding logic here.

    bool h_dup = false;
    set<int> seen;
    for(int v : ch) {
        for(int val : st[v]) {
            if(seen.count(val)) {
                h_dup = true;
                break;
            }
            seen.insert(val);
        }
        if(h_dup) break;
    }

    dp[u] = 0;
    for(int v : ch) {
        dp[u] += dp[v];
    }

    if(h_dup) {
        map<int, int> fq;
        for(int v : ch) {
            for(int val : st[v]) {
                fq[val]++;
            }
        }
        
        int mx_c = 0;
        for(auto& it : fq) mx_c = max(mx_c, it.second);
        
        for(auto& it : fq) {
            if(it.second == mx_c) st[u].insert(it.first);
        }
        dp[u] += ch.size() - mx_c;
    } 
    else {
        // Naive merge. No swap(). 
        // O(N^2) insertions on deep trees.
        for(int v : ch) {
            for(int val : st[v]) {
                st[u].insert(val);
            }
        }
        dp[u] += ch.size() - 1;
    }
}

void solve() {
    cin >> n;
    for(int i=1; i<=n; i++) cin >> a[i];
    
    for(int i=1; i<=n-1; i++) {
        int u, v; 
        cin >> u >> v;
        g[u].pb(v);
        g[v].pb(u);
    }

    dfs(1, 0, 0);

    int ans = dp[1];
    if(st[1].find(0) == st[1].end()) ans++;
    cout << ans;
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    solve();
    return 0;
}