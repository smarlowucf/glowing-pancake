provider "aws" {
  region = var.region
}

data "aws_ami" "leap" {
  most_recent = true

  filter {
    name   = "name"
    values = var.ami_name_match
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  owners = var.ami_owners
}

resource "aws_key_pair" "default" {
  key_name = "pancakekey"
  public_key = file("~/.ssh/pancake.pub")
}

data "http" "myip" {
  url = "https://ipv4.icanhazip.com"
}

resource "aws_security_group" "default" {
  name = "allowflask"
  description = "Allow Flask and SSH"

  ingress {
    from_port = 5000
    to_port = 5000
    protocol = "tcp"
    cidr_blocks = ["${chomp(data.http.myip.body)}/32"]
  }

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["${chomp(data.http.myip.body)}/32"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "pancake" {
  ami           = data.aws_ami.leap.id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.default.key_name
  security_groups = [aws_security_group.default.name]
}

resource "null_resource" "configure-pancake" {
  depends_on = [aws_instance.pancake]

  triggers = {
    instance_id = aws_instance.pancake.id
  }

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file("~/.ssh/pancake")
    host        = element(aws_instance.pancake.*.public_ip, 0)
  }

  provisioner "remote-exec" {
    inline = [
      "sudo zypper -n refresh",
    ]
  }

  provisioner "remote-exec" {
    inline = [
      "sudo zypper -n in salt-minion",
      "sudo sed -i 's/#file_client: remote/file_client: local/' /etc/salt/minion",
      "sudo systemctl start salt-minion",
      "sudo systemctl enable salt-minion",
    ]
  }

  provisioner "file" {
    source      = "salt"
    destination = "/home/ec2-user/salt"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo ln -s /home/ec2-user/salt/ /srv/salt",
      #"sudo salt-call --local state.apply"
    ]
  }

  provisioner "remote-exec" {
    inline = [
      "sudo systemctl restart apache2"
    ]
  }
}
/*
resource "null_resource" "test-pancake" {
  depends_on = [null_resource.configure-pancake]

  provisioner "local-exec" {
    command = "pytest -v --ssh-config ssh.conf --hosts ${element(aws_instance.pancake.*.public_ip, 0)} ../tests/test_pancake.py"
  }
}*/

output "ip" {
  value = element(aws_instance.pancake.*.public_ip, 0)
}
