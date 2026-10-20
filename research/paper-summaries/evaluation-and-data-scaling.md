# Evaluation Practice and Data Scaling

## Robot Learning as an Empirical Science (Kress-Gazit et al., 2024)

**Robot Learning as an Empirical Science: Best Practices for Policy Evaluation.** Hadas Kress-Gazit, Kunimatsu Hashimoto, Naveen Kuppuswamy, Paarth Shah, Phoebe Horgan, Gordon Richardson, Siyuan Feng, Benjamin Burchfiel (Cornell University and Toyota Research Institute). arXiv:2409.09491, 2024. **Status:** preprint. [arXiv](https://arxiv.org/abs/2409.09491)

**In our words.** The authors observe that physical robot-learning papers mostly report a single success rate over a handful of trials, often without stating initial conditions. They argue for treating evaluation as experimental science: state the experimental conditions explicitly (learned policies are highly sensitive to the deployment environment), report metrics that complement success rate, analyse results statistically, and describe failure modes qualitatively. They illustrate this with physical-robot evaluations of several learned manipulation policies.

**Applied here:** the [evaluation protocol](../../docs/evaluation.md) logs fixed conditions, defines position sets, uses partial credit and a failure taxonomy, and reports Wilson intervals.

## Data Scaling Laws in Imitation Learning (Lin et al., ICLR 2025)

**Data Scaling Laws in Imitation Learning for Robotic Manipulation.** Fanqi Lin, Yingdong Hu, Pingyue Sheng, Chuan Wen, Jiacheng You, Yang Gao. ICLR 2025 (oral). arXiv:2410.18647. **Status:** peer-reviewed. [arXiv](https://arxiv.org/abs/2410.18647) · [project](https://data-scaling-laws.github.io/)

**In our words.** Using a hand-held gripper interface (UMI), the authors collected over 40,000 demonstrations and ran over 15,000 real-world rollouts to study how a single-task policy's generalization grows with data. Generalization to new environments and objects followed roughly a **power law in the number of environments and objects**, while extra demonstrations in the same environment showed diminishing returns. From this they derive a collection strategy (many environment–object pairs, modest demonstrations each) and report about 90 % success in novel environments with unseen objects for two tasks, using data collected by four people in one afternoon.

**Applied here:** when expanding the dataset, add new cube positions (and later new objects and tray positions) before adding more repetitions of existing ones, while keeping roughly 10 demonstrations per condition, as the SmolVLA guide suggests.

## robomimic (Mandlekar et al., CoRL 2021)

**What Matters in Learning from Offline Human Demonstrations for Robot Manipulation.** Ajay Mandlekar et al. CoRL 2021. arXiv:2108.03298. **Status:** peer-reviewed. [arXiv](https://arxiv.org/abs/2108.03298)

**In our words.** A large controlled study of offline learning from human demonstrations, in simulation and on real robots. Key takeaways relevant here: demonstration quality matters a great deal (data from more proficient operators trains better policies than mixed-quality data); the choice of observation space and hyperparameters has large effects; and the policy checkpoint chosen by validation loss is often not the best by task success.

**Applied here:** select checkpoints by robot evaluation, not by loss; keep demonstrations consistent; discard poor ones.
