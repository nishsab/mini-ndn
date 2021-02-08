# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
ln -s /vagrant /home/vagrant/mini-ndn

# Check if install.sh is present or someone just copied the Vagrantfile directly
if [[ -f /home/vagrant/mini-ndn/install.sh ]]; then
  pushd /home/vagrant/mini-ndn
else
  # Remove the symlink
  rm /home/vagrant/mini-ndn
  git clone --depth 1 https://github.com/named-data/mini-ndn.git
  pushd mini-ndn
fi
./install.sh -qa

sudo apt-get update
sudo apt-get install emacs

mkdir /home/vagrant/src
cd /home/vagrant/src
git clone https://github.com/nishsab/ndn-svs.git
cd /home/vagrant/src/ndn-svs
./waf configure --enable-static --disable-shared --with-examples
./waf 

sudo mkdir /opt/svs
sudo chown vagrant /opt/svs
mkdir /opt/svs/logs
mkdir /opt/svs/logs/svs
mkdir /opt/svs/stats
mkdir /opt/svs/example-security
cp /home/vagrant/src/ndn-svs/example-security/validation.conf /opt/svs/example-security/
ln -sf /home/vagrant/src/ndn-svs/build/examples/chat2 /opt/svs/chat

mkdir /home/vagrant/logs
mkdir /home/vagrant/logs/svs
ln -sf /home/vagrant/src/ndn-svs/build/examples/chat2 /home/vagrant/chat
mkdir /home/vagrant/example-security
cp /home/vagrant/src/ndn-svs/example-security/validation.conf /home/vagrant/example-security/validation.conf

SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.provision "shell", privileged: false, inline: $script
  config.vm.provider "virtualbox" do |vb|
    vb.name = "mini-ndn_box"
    vb.memory = 4096
    vb.cpus = 4
  end
end
