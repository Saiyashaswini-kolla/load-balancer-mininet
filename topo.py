from mininet.topo import Topo

# Mininet simulation

class LoadBalancerTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)
        # Add client
        client = self.addHost('client')
        # Add load balancer
        lb = self.addHost('lb')

        # Add servers
        s1 = self.addHost('s1')
        s2 = self.addHost('s2')
        s3 = self.addHost('s3')
        s4 = self.addHost('s4')
        s5 = self.addHost('s5')
        s6 = self.addHost('s6')
        s7 = self.addHost('s7')
        s8 = self.addHost('s8')

        # Add switches
        sw1 = self.addSwitch('sw1')
        sw2 = self.addSwitch('sw2')
        sw3 = self.addSwitch('sw3')

        # Connect client to switch
        self.addLink(client, sw1)
        self.addLink(sw1,sw3)

        # Connect load balancer to switches
        self.addLink(lb, sw3)

        # Connect servers to switches
        self.addLink(s1, sw1)
        self.addLink(s2, sw1)
        self.addLink(s3, sw1)
        self.addLink(s4, sw1)
        self.addLink(s5, sw2)
        self.addLink(s6, sw2)
        self.addLink(s7, sw2)
        self.addLink(s8, sw2)

        self.addLink(sw3,sw2)

topos = {'loadbalancer': (lambda: LoadBalancerTopo())}
