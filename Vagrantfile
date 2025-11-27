Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-24.04"


  # Default provider settings (for every VM)
  config.vm.provider :libvirt do |v|
    v.memory = 2048
    v.cpus = 2
  end

  config.vm.synced_folder ".", "/home/vagrant/AStream",
    type: "rsync",
    rsync__exclude: [".git/", "tmp/", ".vagrant/", "TEMP_*", "*.log", "ASTREAM_LOGS"],
    rsync__args: ["--verbose", "--archive", "--delete", "--copy-links"]
  
  config.vm.provision "shell", inline: <<-SHELL
    apt update
    apt install -y python3 python3-pip git vim tmux wget net-tools iputils-ping curl rsync
  SHELL

  BRIDGE_IFACE = "enp3s0"
  
  # ---- CLIENT NODE ----
  config.vm.define "client" do |node|
    node.vm.hostname = "client"

    # Private network for lab
    node.vm.network :private_network, ip: "192.168.56.11"
    # node.vm.network :public_network, dev: BRIDGE_IFACE, mode: "bridge"  
  end

  # ---- PROXY NODE ----
  config.vm.define "proxy" do |node|
    node.vm.hostname = "proxy"

    node.vm.network :private_network, ip: "192.168.56.12"
    # node.vm.network :public_network, dev: BRIDGE_IFACE, mode: "bridge"  

    node.vm.provision "shell", inline: <<-SHELL
      echo "Enabling IPv4 forwarding..."
      sed -i 's/^#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
      sysctl -w net.ipv4.ip_forward=1
      sysctl -p /etc/sysctl.conf
    SHELL
  end

  # ---- SERVER NODE ----
  config.vm.define "server" do |node|
    node.vm.hostname = "server"

    node.vm.network :private_network, ip: "192.168.56.13"
    # node.vm.network :public_network, dev: BRIDGE_IFACE, mode: "bridge"  
  end
end

