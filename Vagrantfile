# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
# workaround for vagrant not being able to run everything as sudo
# https://github.com/opscode/bento/pull/201
sed -i -e 's/%sudo\tALL=NOPASSWD:ALL/%sudo\tALL=(ALL) NOPASSWD:ALL/g' /etc/sudoers
SCRIPT

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "chef/ubuntu-14.04"

    config.vm.network "forwarded_port", guest: 80, host: 8080
    config.ssh.forward_agent = true

    config.vm.provision "shell", inline: $script
end
