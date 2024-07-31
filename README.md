# Note: I made this a long time ago, and i didn't think about optimizing it as I was just exploring the topic, I may eventually rewrite this all in go.

requirements: fucking none, i made it all using standard libraries.


# AIBullshit
A basic library to let you create moder bullshit AI projects, which lets you build neural networks however you want, as a pay off you have to manually select which neural network to keep for the next generation.

IGNORE SPELLING MISTAKES IN SOURCE FILE PLEASSSEEE

# Basic Usecases

A bad example, good luck figuring it out.
```py
from AI import * # Bad practive, but f u

# predefine the amounts of 
test_network_template = NetworkTemplate(3, 6, 100, 4, 10) # 3 inputs, 6 outputs, 100 'braincell' limit (pretty close to the average orange cat (exagerated)), 4 'startspread' (start mustation), 10 max layers (between in and output)

network1 = test_network_template.network # don't call it, it's a property
network2 = test_network_template.network

networks = [network1, network2]

for network in networks:
  print(network.process([0, 4, 2])) # will print out 6 random numbers for each network, duh

# let's say by bull shit means network1 was a good girl/boy/dog/cat/ect.

off_spring1, off_spring2 = network1.copy(), network1.copy()

off_spring2.mutate(50, 4) # 50 is the maximum random amount of changes done to the network, a change for example can be either the adding or removal of a node/neuron, or a random connection or even a random weight redistribution

#off spring1 is exactly like it's parent, off spring 2 is just a little different (trying so hard not to make a edgy joke)

# let's save both ffs
save_network(off_spring1, "offspring1.json") # saved as json
save_network(off_spring2, "offspring2.json")

off1 = load_network("offspring1.json", test_network_template.brainCellLimit) # brainCellLimit is important if you want to specify further mutate your network, if not leave at default 10
off2 = load_network("offspring2.json")

package("offspring1.json", "offspring1.AIBSdump") # or whatever extension you want, it honestly just uses zlib to compress the file, feel free to delete the json afterwards if you plan to not use the network for a long time and already have storage issues 
package("offspring2.json", "offspring2.AIBSdump")

# and if you want to use it again, and only have the dump file:
unpackage("offspring1.AIBSdump", "offspring1.json")
unpackage("offspring2.AIBSdump", "offspring2.json")
```
